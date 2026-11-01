# Live session · Deploying on AWS with Docker, ECR, ECS and Fargate

The step-by-step from the session, grouped into phases, with the reason behind each step. The architecture choice is explained in [01_deployment_architectures.md](01_deployment_architectures.md).

## The big picture

```
YOUR LAPTOP                              AWS
───────────                              ───
code ──docker build──► image ──docker push──► ECR (image storage)
                                               │ pulled by
                                               ▼
                         ECS cluster ─► service (keep 1 running) ─► task on Fargate
                                                                      │ runs
user ─► ALB :80 ─► target group ─► task IP :8000 ─► uvicorn ─► FastAPI ─► LLM APIs
```

| Phase | What happens | Where |
|---|---|---|
| 1 | Make the app container-ready | Laptop |
| 2 | Package it as a Docker image and test it | Laptop |
| 3 | Give your terminal access to AWS | Laptop + IAM |
| 4 | Upload the image | ECR |
| 5 | Run it | ECS + Fargate |
| 6 | Give it a stable address | Application Load Balancer |
| 7 | Give it the API key | ECS task definition |
| 8 | Ship a new version | All of the above |

## Phase 1 · Make the app container-ready

**Add the serving dependencies** to `requirements.txt`:

| Package | Why |
|---|---|
| `fastapi` | The web framework |
| `uvicorn` | The server process that runs FastAPI |
| `python-multipart` | Needed for file uploads (`UploadFile`); FastAPI errors without it |

**Create the `data/` folder at startup** (after the imports in `app.py`):

```python
os.makedirs("data", exist_ok=True)
```

A container starts from a clean copy of the image every time. If the code writes to `data/` and the folder isn't there, saving uploads fails. `exist_ok=True` makes it safe to run when the folder already exists.

> **Container storage is temporary.** Anything written inside a running container (uploads, output Excel files) is **lost when the task stops or is replaced**, and isn't shared between two running copies. That's fine for a demo that returns the file in the response. For anything you need to keep, write to S3.

**Add CORS middleware** (from the guide):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

CORS (Cross-Origin Resource Sharing) is a **browser** rule. A web page from one origin (e.g. `https://myfrontend.com`) may only call an API on another origin if the API's response headers allow it. This middleware adds those headers.

> **Correction to the guide:** CORS isn't needed for `/docs` to work. Swagger UI is served by the same app, so it's the same origin. You need CORS only when a separate frontend calls the API from a browser. `curl`, Python scripts and Postman ignore CORS completely. Also, `allow_origins=["*"]` together with `allow_credentials=True` is risky: browsers forbid `*` with credentials, so Starlette sends back whichever origin asked, which lets **any** website make logged-in requests. For production, list the real frontend origins explicitly.

**Run it once the way the container will:**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

`--host 0.0.0.0` means "accept connections on every network interface". The default, `127.0.0.1`, only accepts connections from the same machine. Inside a container, that means *from inside the container only*, so Docker's port forwarding and AWS's load balancer couldn't reach the app.

## Phase 2 · Package it with Docker

**`.dockerignore`** controls what `COPY . .` is allowed to copy into the image:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.git
.vscode
logs/
data/
```

`.env` is the important line: **API keys must never be baked into an image**. Anyone who can pull the image could read them.

**`Dockerfile`:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p data logs
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Line | Meaning |
|---|---|
| `FROM python:3.11-slim` | Start from a small official Linux image with Python 3.11 |
| `WORKDIR /app` | All following commands run in `/app` inside the image |
| `COPY requirements.txt .` then `RUN pip install` | Install packages **before** copying the code. Docker caches each step, so when only your code changes, the slow install step is reused |
| `--no-cache-dir` | Don't keep pip's download cache, so the image is smaller |
| `COPY . .` | Copy the project (minus everything in `.dockerignore`) |
| `RUN mkdir -p data logs` | Create the working folders in the image |
| `EXPOSE 8000` | **Documentation only.** It doesn't open or publish anything; `-p` or the cloud platform does that |
| `CMD [...]` | The command that runs when a container starts |

**Build, check, run:**

```bash
docker build -t qa-evaluator-app .                         # build and name the image
docker images                                              # qa-evaluator-app should be listed
docker run -p 8000:8000 --env-file .env qa-evaluator-app   # run it locally
```

Then open `http://localhost:8000/docs`.

- **`-p 8000:8000`** is `LAPTOP_PORT:CONTAINER_PORT`. Without it, nothing outside the container can reach the app. The full explanation, with the two connections involved, is in this project's [README](../README.md#how-a-request-reaches-the-app).
- **`--env-file .env`** injects the variables into the running container at start-up. They are never part of the image.
- **`.env` must have no spaces around the variable name.** `OPENAI_API_KEY =abc` fails with *variable 'OPENAI_API_KEY ' contains whitespaces*. Write `OPENAI_API_KEY=abc`.

## Phase 3 · Connect your terminal to AWS

```bash
aws --version                  # is the AWS CLI installed?
aws configure                  # paste access key, secret key, region (us-east-1), output (json)
aws sts get-caller-identity    # prints your account and user if login worked
```

The guide's steps:

1. Create an IAM user `ecs-deployment-user` with **AdministratorAccess**.
2. Create an access key for it.
3. Paste the key into `aws configure`.

> **Correction to the guide:** AdministratorAccess on a user with a long-lived access key is acceptable for a throwaway lab, never beyond it. Anyone who finds that key controls the whole account. For anything real, give the user only the permissions it needs (ECR push, ECS update), or skip access keys entirely with `aws configure sso` (IAM Identity Center), which issues short-lived credentials. Never commit `~/.aws/credentials` or paste keys into chat.

## Phase 4 · Upload the image to ECR

**ECR (Elastic Container Registry)** is a private Docker Hub inside your AWS account.

1. **Create a private repository** in the ECR console called `qa-evaluator-app`, and copy its **URI**. It has the form `<account-id>.dkr.ecr.<region>.amazonaws.com/qa-evaluator-app`.
2. **Log Docker in to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ECR_URI>
   ```
   Expect `Login Succeeded`. The AWS CLI produces a temporary password, and Docker uses it.
3. **Tag the image** with the ECR address:
   ```bash
   docker tag qa-evaluator-app:latest <ECR_URI>:latest
   ```
   A tag is just **another name for the same image**. `docker images` will show two rows with the same IMAGE ID, and no disk space is used twice. Docker reads the registry address from the name to know where to push.
4. **Push:**
   ```bash
   docker push <ECR_URI>:latest
   ```
   Expect `latest: digest: sha256:...`. Then refresh the ECR console to see the image, its `latest` tag and the push time.

| Error | Cause | Fix |
|---|---|---|
| `No such image: qa-evaluator-app:latest` | The name in `docker tag` doesn't match the name you built with | Check `docker images` and use that exact name |
| `denied: Your authorization token has expired` | The ECR login token lasts **12 hours** | Run the login command again, then push straight away |

## Phase 5 · Run it on ECS with Fargate

First, once per account, let ECS manage resources on your behalf:

```bash
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```

If it says the role already exists, that's fine.

### The four ECS building blocks

| Piece | What it is | Analogy |
|---|---|---|
| **Cluster** | A logical group where your containers run | The kitchen |
| **Task definition** | The blueprint: image, CPU/memory, port, environment variables, logging | The recipe |
| **Task** | One running copy of that blueprint | One dish being cooked |
| **Service** | Keeps the chosen number of tasks running, and replaces any that crash | The chef who keeps N dishes ready at all times |

**Fargate or EC2?** ECS can run tasks on EC2 servers that you manage, or on **Fargate**, where AWS provides the compute. The session chose Fargate: no servers to patch, simpler to start with, and still production-grade.

### Step 1 · Cluster

ECS console → **Create cluster**:

- Name: `qa-evaluator-cluster`.
- Infrastructure: **AWS Fargate (serverless)**.
- Leave the rest as default, and wait for Status = **Active**.

Nothing runs yet. The cluster is just the space the tasks will live in.

### Step 2 · Task definition

ECS → Task definitions → **Create new task definition**:

| Setting | Value |
|---|---|
| Family | `AI-qa-evaluator-task` |
| Launch type | AWS Fargate |
| OS / architecture | Linux / X86_64 |
| CPU / memory | Defaults |
| Task execution role | `ecsTaskExecutionRole` (AWS usually creates it) |
| Container name | `qa-evaluator-container` |
| Image URI | `<ECR_URI>:latest` |
| Port mapping | 8000 / TCP |

There are two different IAM roles here, and they're easy to mix up:

| Role | Used by | For |
|---|---|---|
| **Task execution role** | ECS itself | Pulling the image from ECR, writing logs to CloudWatch, reading secrets at start-up |
| **Task role** | **Your Python code** | Calling other AWS services from the app, e.g. reading from S3. Not needed here |

> **Architecture must match.** The task runs on X86_64. An image built on an Apple Silicon Mac is ARM and fails with `exec format error`. Build it with `docker build --platform linux/amd64 ...`. On an Intel/AMD Linux laptop it already matches.

### Step 3 · Service

Open the cluster → Services → **Create**:

| Setting | Value | Why |
|---|---|---|
| Compute | Fargate | |
| Task definition | `AI-qa-evaluator-task`, revision LATEST | |
| Service name | `qa-evaluator-service` | |
| Desired tasks | 1 | One running container |
| VPC / subnets | Defaults | |
| Security group | New. Inbound Custom TCP **8000** from `0.0.0.0/0` | Lets the internet reach the container's port |
| Public IP | **On** | Needed to reach it from your browser, **and** for the task to pull its image from ECR (default public subnets have no other route out) |
| Load balancer | None for now | Added in phase 6 |

Wait until the task shows **Running**. Open it, copy the **public IP**, and visit `http://PUBLIC_IP:8000/docs`.

> **The public IP isn't stable.** Every time the task is replaced (a crash, a redeploy, a new revision), it gets a new IP. That's the main reason for phase 6.

## Phase 6 · A stable address with an Application Load Balancer

| Without ALB | With ALB |
|---|---|
| The address changes on every redeploy | One fixed DNS name |
| Users hit the container directly | Users hit the ALB, which forwards to healthy containers only |
| One container | Can spread traffic over many containers, the basis for auto scaling |
| No health checks | Unhealthy containers are taken out of rotation automatically |

### The pieces

```
internet ─► ALB listener HTTP:80 ─► target group (type IP, port 8000, health check) ─► task IPs
```

| Piece | Job |
|---|---|
| **Load balancer** | The public entry point, with a DNS name like `qa-evaluator-alb-123.us-east-1.elb.amazonaws.com` |
| **Listener** | "Accept traffic on HTTP port 80" |
| **Target group** | The list of backends plus the health-check rule. The target type must be **IP**, because each Fargate task gets its own IP address |
| **Health check** | The ALB calls a path (here `/`) and expects HTTP 200. Targets that fail are marked unhealthy and get no traffic |

### Steps

1. **Create the ALB.** EC2 console → Load balancers → Create → **Application Load Balancer**:
   - Name `qa-evaluator-alb`, scheme **Internet-facing**, IPv4.
   - Default VPC, and **all** subnets.
   - A security group allowing **HTTP 80 from `0.0.0.0/0`**.
2. **Create the target group** (from the same page, in a new tab):
   - Target type **IP addresses**, name `qa-evaluator-target-group`.
   - HTTP, port **8000**, default VPC, health check path `/`.
   - Go back to the ALB tab and select this target group for the listener.
3. **Attach the ALB to the ECS service.** Open the service → **Update** → Load balancing:

   | Setting | Value |
   |---|---|
   | Type | Application Load Balancer |
   | Load balancer | `qa-evaluator-alb` |
   | Listener | HTTP:80 |
   | Target group | `qa-evaluator-target-group` |
   | Container / port | `qa-evaluator-container` / 8000 |

   ECS then redeploys the task, registers its IP in the target group, and the ALB starts health checks. This takes about 2–5 minutes.
4. **Verify:** EC2 → Target groups → `qa-evaluator-target-group` → Targets should show **healthy**. Then open `http://<ALB_DNS>/docs`.

> **Correction to the guide: the security group chain.** The guide reuses one security group for both the ALB and the task, which leaves port 8000 open to the whole internet. The usual setup uses two groups:
> - **ALB group:** allows port 80 from anywhere.
> - **Task group:** allows port 8000 **only from the ALB's security group**.
>
> Then the container can only be reached through the load balancer.

> **Watch out for long requests.** The ALB closes a connection that sends no data for **60 seconds** (the "idle timeout"), and the client gets a **504**. A big transcript file can take longer than that. Raise the idle timeout in the ALB's attributes, or move to "submit job, fetch result later" for big batches.

Use a cheap endpoint for the health check: this app's `/ping` is better than a page that does real work.

## Phase 7 · Give the container its API key

The `.env` file is excluded from the image (phase 2), so ECS starts the container **without** your keys. You add them to the task definition. You don't need to rebuild or push the image.

1. ECS → Task definitions → `AI-qa-evaluator-task` → latest revision → **Create new revision**. Revisions can't be edited; every change makes a new one.
2. Container `qa-evaluator-container` → **Environment variables** → Add:
   - Name: **exactly** what the code reads, e.g. `OPENAI_API_KEY`.
   - Value: the key, with no quotes and no spaces.
   - Add **every** variable the code reads. This app's `llm_loader.py` also requires `LLM_PROVIDER` (`openai` or `gemini`).
3. Create the revision.
4. **Point the service at the new revision.** Creating a revision changes nothing on its own. Service → Update → choose the new revision → **Update service**. ECS starts a new task with the new settings and stops the old one.
5. Test the feature that calls the LLM through `http://<ALB_DNS>/docs`.

If it still fails, check these:
- Does the variable name exactly match `os.getenv(...)` in the code?
- Is the service on the **new** revision?
- What do the task's **Logs** tab or CloudWatch say?

> **Plain environment variables are visible** to anyone who can view the task definition. In production, store the key in **AWS Secrets Manager** (or SSM Parameter Store). In the container definition, use `secrets` (`valueFrom` = the secret's ARN) instead of `environment`, and allow the **task execution role** `secretsmanager:GetSecretValue`. The app still reads it with `os.getenv`, so no code change is needed.

Changing your local `.env` later does nothing to AWS. A new key means a new revision and another service update.

## Phase 8 · Shipping a new version (not covered in the AWS guide)

```bash
docker build -t qa-evaluator-app .
docker tag qa-evaluator-app:latest <ECR_URI>:latest
docker push <ECR_URI>:latest
aws ecs update-service --cluster qa-evaluator-cluster --service qa-evaluator-service --force-new-deployment
```

Pushing a new `latest` doesn't restart anything. The task definition still says `:latest`, so ECS doesn't know the image changed. `--force-new-deployment` makes it start fresh tasks, which pull the new image.

It's safer to push a **unique tag per release**, e.g. `:v2` or the git commit ID, and create a task definition revision that points to it. Then you always know exactly what's running, and rolling back means selecting the previous revision.

## Troubleshooting map

| Symptom | Likely cause |
|---|---|
| `poorly formatted environment ... contains whitespaces` | Spaces around `=` in `.env` |
| `No such image` on `docker tag` | Wrong source image name |
| `authorization token has expired` on push | ECR login is older than 12 h; log in again |
| Task stops right after starting | App crashed at start-up, often a missing environment variable. Check the task's "Stopped reason" and logs |
| `CannotPullContainerError` | No public IP, or no network route to ECR |
| `exec format error` | ARM image on an X86_64 task; rebuild with `--platform linux/amd64` |
| Target group shows **unhealthy** | Wrong health-check path, wrong port, or the task's security group blocks the ALB |
| **504** from the ALB | The request took longer than the ALB idle timeout (60 s) |
| Works on the IP, not the ALB | Service not attached to the target group, or the ALB security group lacks port 80 |

> **Takeaway:** image (Docker) → registry (ECR) → blueprint (task definition) → keeper (service) → front door (ALB). Secrets go in at run time, never in the image. Every change creates a new revision, and the service must be told to use it.

## Check yourself

1. Why does `uvicorn` need `--host 0.0.0.0` inside a container?
2. What is the difference between a task definition, a task and a service?
3. You pushed a fixed image as `:latest`, but the app still behaves the old way. Why, and what's the fix?
4. Why must the target group's target type be **IP** for Fargate?
5. You add `OPENAI_API_KEY` in a new task definition revision, but the app still says the key is missing. What did you forget?
6. Which IAM role pulls the image from ECR, and which one would your code use to read from S3?
7. A user uploads a large file and gets a 504 after exactly one minute. What's happening?
