# Live session · The same deployment on Azure and Google Cloud

The session shared Azure and GCP versions of the AWS guide. The app, the `Dockerfile` and the `.dockerignore` are **identical**. Only the registry, the runtime service and the CLI change. These notes focus on what's different. The shared steps are in [02_deploying_on_aws_ecs_fargate.md](02_deploying_on_aws_ecs_fargate.md).

## One table to map the three clouds

| Job | AWS (session) | Azure | Google Cloud |
|---|---|---|---|
| Group related resources | Region + tags | **Resource group** | **Project** |
| Store the image | ECR | **Azure Container Registry (ACR)** | **Artifact Registry** |
| Run the container | ECS + Fargate | **Azure Container Apps** | **Cloud Run** |
| Public URL | ALB (HTTP), plus ACM certificate for HTTPS | Built-in ingress, **HTTPS included** | Built-in, **HTTPS included** |
| Keep the API key | Task definition env var, or Secrets Manager | Container App **secret** → env var | **Secret Manager** → env var |
| CLI | `aws` | `az` | `gcloud` |
| Log Docker in | `aws ecr get-login-password \| docker login ...` | `az acr login --name <acr>` | `gcloud auth configure-docker <region>-docker.pkg.dev` |
| Logs | CloudWatch | `az containerapp logs show` | `gcloud run services logs read` |

**Why Azure and GCP need no separate load balancer.** Container Apps and Cloud Run are higher-level services: one command gives you a stable `https://` URL, load balancing and scaling. On AWS, ECS is a lower-level building block, so you add the ALB (and a certificate for HTTPS) yourself. That's more work, but also more control.

## The flow every cloud shares

```
1. test locally (uvicorn --host 0.0.0.0 --port 8000)
2. docker build
3. log in to the cloud CLI
4. create a registry  →  log Docker in  →  docker tag  →  docker push
5. deploy the image, telling the platform the app listens on port 8000
6. add API keys as secrets / env vars (never in the image)
7. open <URL>/docs and check the logs
8. next release: build → tag → push → redeploy
```

## Azure: Container Apps + ACR

| Step | Command (names from the guide) |
|---|---|
| Sign in | `az login` → `az account show` (pick a subscription with `az account set --subscription <id>`) |
| Resource group | `az group create --name qa-evaluator-rg --location eastus` |
| Registry | `az acr create --resource-group qa-evaluator-rg --name <uniquename> --sku Basic` |
| Log Docker in | `az acr login --name <uniquename>` |
| Tag + push | `docker tag qa-evaluator-app:latest <uniquename>.azurecr.io/qa-evaluator-app:latest` → `docker push ...` |
| One-time setup | `az provider register --namespace Microsoft.App` (and `Microsoft.OperationalInsights`), `az extension add --name containerapp --upgrade` |
| Environment | `az containerapp env create --name qa-evaluator-env --resource-group qa-evaluator-rg --location eastus` |
| Deploy | `az containerapp create ... --image <acr>/qa-evaluator-app:latest --target-port 8000 --ingress external --min-replicas 1 --max-replicas 1` |
| URL | `az containerapp show ... --query properties.configuration.ingress.fqdn` → `https://<fqdn>/docs` |
| API key | `az containerapp secret set ... --secrets openai-api-key=<key>` then `az containerapp update ... --set-env-vars OPENAI_API_KEY=secretref:openai-api-key` |
| New release | push the image, then `az containerapp update ... --image <acr>/qa-evaluator-app:<tag>` |
| Delete everything | `az group delete --name qa-evaluator-rg --yes --no-wait` |

Terms:

- **Resource group:** a folder for related resources. Deleting the group deletes everything inside it, which makes cleanup a single command.
- **ACR name:** must be **globally unique**, lowercase letters and digits only. It becomes `<name>.azurecr.io`.
- **Container Apps environment:** the shared boundary (network and logging) that one or more container apps run in. It's roughly the ECS cluster.
- **`--target-port 8000`:** the port the app listens on **inside** the container.
- **`--ingress external`:** make the app reachable from the internet.
- **Secret vs environment variable:** `openai-api-key` is the secret's name in Azure. `OPENAI_API_KEY` is the variable your code reads. `secretref:` connects the two.
- **Revisions:** every configuration change creates a new revision, just like ECS task definitions. Wait for it to become active before testing.

> **Correction to the guide:** the deploy command reads the registry password with `az acr credential show`. That only works if the registry's **admin user is enabled**, which `az acr create` doesn't do by default. Enable it with `az acr update --name <uniquename> --admin-enabled true`, or better, as the guide itself suggests for production, give the container app a **managed identity** with pull access to the registry.

> `--min-replicas 1` keeps one copy running, and billed, around the clock. `--min-replicas 0` lets the app scale to zero when idle. That's cheaper, but the first request after a quiet period is slow while it starts.

> The first link in the guide's documentation list doesn't look like an official Microsoft address. Use the `learn.microsoft.com` links in the same list instead.

## Google Cloud: Cloud Run + Artifact Registry

| Step | Command (names from the guide) |
|---|---|
| Sign in + project | `gcloud auth login` → `gcloud config set project <PROJECT_ID>` (the ID, not the display name; billing must be on) |
| Enable APIs | `gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com` |
| Registry | `gcloud artifacts repositories create qa-evaluator-repo --repository-format=docker --location=us-central1` |
| Log Docker in | `gcloud auth configure-docker us-central1-docker.pkg.dev` |
| Tag + push | `docker tag qa-evaluator-app:latest us-central1-docker.pkg.dev/<PROJECT_ID>/qa-evaluator-repo/qa-evaluator-app:latest` → `docker push ...` |
| Deploy | `gcloud run deploy qa-evaluator-service --image <path> --region us-central1 --port 8000 --allow-unauthenticated` |
| URL | printed by the deploy, or `gcloud run services describe ... --format="value(status.url)"` |
| API key | Secret Manager, below |
| Logs | `gcloud run services logs read qa-evaluator-service --region us-central1 --limit 50` |
| New release | build → tag → push → run the same `gcloud run deploy` again |

Terms:

- **Image path format:** `REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE:TAG`. The address itself tells Docker which registry, project and repository to use.
- **`--port 8000`:** Cloud Run sends traffic to this port in the container. It also sets the `PORT` environment variable to 8000.
- **`--allow-unauthenticated`:** anyone with the URL can call it. Leave it off for private services.

**API key through Secret Manager** (the guide's recommended route):

```bash
gcloud services enable secretmanager.googleapis.com
echo -n "<key>" | gcloud secrets create openai-api-key --data-file=-
gcloud secrets add-iam-policy-binding openai-api-key \
    --member="serviceAccount:<service-account-email>" --role="roles/secretmanager.secretAccessor"
gcloud run services update qa-evaluator-service --region us-central1 \
    --update-secrets=OPENAI_API_KEY=openai-api-key:latest
```

- `echo -n` stops a newline being saved as part of the key.
- The Cloud Run service runs as a **service account**, GCP's identity for a program. It needs the `secretAccessor` role to read the secret, which is the same idea as the ECS task execution role reading Secrets Manager. If the `describe` command shows no service account, the service uses the project's default Compute Engine account, `<project-number>-compute@developer.gserviceaccount.com`.
- `:latest` here means the latest **version of the secret**, not a Docker tag.

## Limits that matter for this app

| Platform | Max time for one HTTP request |
|---|---|
| AWS ALB | Idle timeout 60 s by default, configurable |
| Azure Container Apps ingress | About 4 minutes |
| Google Cloud Run | 5 minutes by default, up to 60 minutes |

A large transcript file can hit any of these. Above a few minutes, switch to "upload → background job → fetch result".

**Image architecture:** all three run `linux/amd64` by default. On an Apple Silicon Mac, build with `docker build --platform linux/amd64 ...`.

**Use a unique tag per release** (`v2`, a git commit ID) instead of always pushing `latest`. Both guides recommend it: you know exactly what's running, and rolling back is easy.

> **Takeaway:** Docker makes the app portable. Moving clouds changes only the registry, the runtime and the CLI. Azure Container Apps and Cloud Run hand you HTTPS and scaling in one command. ECS + ALB asks you to wire those up yourself, in return for more control.

## Check yourself

1. What is the Azure and GCP equivalent of ECR? Of ECS + Fargate?
2. Why do Container Apps and Cloud Run not need a separately created load balancer?
3. In `OPENAI_API_KEY=secretref:openai-api-key`, which name does your Python code use?
4. Your Cloud Run service can't read its secret. Which identity is missing which role?
5. What does `--min-replicas 0` save, and what does it cost you?
