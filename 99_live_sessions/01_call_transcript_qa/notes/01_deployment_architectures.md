# Live session · Deployment architectures for GenAI apps

## Why deployment is its own topic

Building the LLM pipeline is only half the job. **Deployment** answers the next question: *how do real users reach this application?*

There is no single right answer. The choice depends on:

- expected **traffic** and how much it varies;
- **scalability** and **reliability** needs;
- **budget**;
- **team size** and how much operations work the team can take on.

The app used throughout the session is this project's QA evaluator:

- a **FastAPI** service;
- that accepts an **uploaded file** (CSV/XLSX of call transcripts);
- runs a **multi-stage LLM pipeline** on it (classify → route → evaluate → report);
- and returns a processed **dataframe** as an Excel file.

Those four facts matter later, when we pick an architecture: uploads, long-running LLM calls and heavy dependencies rule some options out.

## The three architectures

| | 1 · Virtual machine | 2 · Containers | 3 · Serverless |
|---|---|---|---|
| **AWS services** | EC2 + Nginx | Docker + ECR + ECS + Fargate + ALB | Lambda + API Gateway |
| **Who manages the server** | You | AWS (Fargate) | AWS |
| **Unit you deploy** | Code copied onto a server | A Docker image | A function (zip or image) |
| **Request path** | User → IP/domain → Nginx → FastAPI → LLM APIs | User → Load balancer → ECS service → Fargate container → FastAPI → LLM APIs | User → API Gateway → Lambda → FastAPI → LLM APIs |

### Architecture 1 · Traditional VM (EC2)

You rent a virtual machine, SSH in, install Python and your packages, and run the app yourself. It's the most transparent option: you can see exactly where the code lives and how a request reaches it.

| Service | Job |
|---|---|
| **Amazon EC2** | The virtual server that runs everything |
| **Nginx** | Reverse proxy: receives every request and forwards it to the app |
| **FastAPI + Uvicorn** | The application and the server process that runs it |
| **Security group** | Firewall: which ports are open, and to whom |
| **Route 53** (optional) | A domain name instead of a raw IP |

**What a reverse proxy is.** The guide defines it as something that "receives requests on behalf of another system". Nginx listens on the public ports (80/443) and passes each request to uvicorn on `127.0.0.1:8000`, which is never exposed to the internet directly. Putting Nginx in front lets you add HTTPS, rate limits, request-size limits and static files without touching the Python app.

| Advantages | Limitations |
|---|---|
| Easiest to understand | Scales poorly: one machine |
| Cheapest at small scale | You patch, monitor and restart the server yourself |
| Full control; debug over SSH | Single point of failure |

**Best for:** learning the fundamentals, small internal tools, low-traffic apps.

### Architecture 2 · Containers (Docker + ECS + Fargate)

You package the app and all its dependencies into a **Docker image** and let AWS run it. You never log in to a server.

| Service | Job |
|---|---|
| **Docker** | Packages the app into a portable image |
| **Amazon ECR** | Private registry that stores the image |
| **Amazon ECS** | Orchestrator: decides what runs, where, and how many copies |
| **AWS Fargate** | Runs the containers without you managing servers |
| **Application Load Balancer** | Single stable address; spreads traffic across containers |
| **Security groups** | Network access control |

The flow: build image → push to ECR → ECS pulls it → Fargate runs it → the ALB routes users to it.

| Advantages | Limitations |
|---|---|
| Industry standard for modern services | Steeper learning curve |
| Scales by adding more containers | You need to know Docker |
| "Works on my machine" = works in the cloud: the image is identical | AWS networking (VPC, subnets, security groups) gets complicated |
| Clean, repeatable deployments | |

**Best for:** production AI services, team deployments, anything that needs to scale. This is the architecture the session deployed. The step-by-step is in [02_deploying_on_aws_ecs_fargate.md](02_deploying_on_aws_ecs_fargate.md).

### Architecture 3 · Serverless (Lambda + API Gateway)

No server and no long-running container. AWS runs your code **only when a request arrives** and bills per request and per millisecond.

| Service | Job |
|---|---|
| **AWS Lambda** | Runs the code on demand |
| **Amazon API Gateway** | The public HTTPS endpoint that triggers Lambda |
| **Mangum** | Adapter that turns an API Gateway event into a normal request FastAPI understands |
| **S3** (optional) | Storage for uploaded and generated files |

| Advantages | Limitations |
|---|---|
| Nothing to manage | **Cold starts**: the first request after idle time is slow, worse with heavy packages like pandas and LangChain |
| Scales automatically, including to zero | **Hard time limits** (see below) |
| Very cheap at low traffic | File uploads are awkward |
| | Harder to debug |

**Why it's a poor fit for this app specifically** (the guide says "timeout limitations"; these are the actual numbers):

- An API Gateway REST API waits about **29 seconds** for Lambda by default. A batch of transcripts with several LLM calls each easily takes longer.
- A Lambda function can run for at most **15 minutes** in total.
- A synchronous Lambda request or response can be at most **6 MB**, which limits upload and download size.

The serverless way around this is asynchronous processing: upload the file to S3, process it in the background, and let the client fetch the result later. That works, but it's a redesign, not just a deployment choice.

**Best for:** lightweight APIs, event-driven jobs (e.g. "a file landed in S3"), spiky or very low traffic.

## Side-by-side comparison (from the session)

| Feature | EC2 | ECS + Fargate | Lambda |
|---|---|---|---|
| Beginner friendly | Excellent | Good | Moderate |
| Industry relevance | Medium | Excellent | High |
| Scalability | Low | High | Very high |
| Reliability | Medium | High | High |
| Cost efficiency | High at first | Medium | High at low traffic |
| Infrastructure you manage | Everything | Very little | None |
| Deployment complexity | Low | Medium | Medium–high |
| Fit for GenAI pipelines | Moderate | Excellent | Moderate |

## Which one for this app, and why

**Docker + ECS + Fargate**, because the app:

- is a long-running FastAPI web service, not a short function;
- accepts file uploads;
- runs multi-stage LLM calls that can take minutes;
- depends on heavy libraries (pandas, LangChain, provider SDKs) that are easiest to ship inside an image.

| Goal | Pick |
|---|---|
| Learn how deployment works | EC2 |
| Ship a production-ready GenAI service | ECS + Fargate |
| A small, cheap, event-driven API | Lambda |

> **Takeaway:** VMs give you control, containers give you repeatability and scale, serverless gives you zero servers but strict limits. Long-running, upload-heavy LLM pipelines fit containers best.

## Check yourself

1. What does Nginx do in the EC2 architecture, and why is uvicorn not exposed to the internet directly?
2. In the container architecture, what is the difference between ECR and ECS?
3. Give two concrete reasons the QA evaluator would struggle on Lambda + API Gateway.
4. A team ships a small webhook that runs a few times a day for under a second. Which architecture fits, and why?
5. What does Fargate remove from your responsibilities compared with ECS on EC2?
