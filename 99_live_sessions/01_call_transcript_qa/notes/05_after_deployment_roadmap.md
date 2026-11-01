# Live session · After deployment: the road to production

The deployment covered containerisation, a registry, orchestration, networking and load balancing. The session closed with what separates a working deployment from a **production** one: automation, scaling, security, observability and cost control.

## The ten topics

| # | Topic | What it is | AWS services / tools | Why it matters |
|---|---|---|---|---|
| 1 | **Logs and monitoring** | See what the app is doing and get alerted when it breaks | CloudWatch Logs, Metrics, Alarms | Without logs, failures are invisible and debugging is guesswork |
| 2 | **Auto scaling** | Add or remove tasks automatically as load changes | ECS Service Auto Scaling, target tracking (e.g. keep CPU at 60 %), min/max task counts | Handles traffic spikes and survives task failures |
| 3 | **Custom domain + HTTPS** | `https://myapp.com` instead of `http://alb-123.elb.amazonaws.com` | Route 53 (DNS), ACM (free TLS certificates), an HTTPS:443 listener on the ALB | Encryption, trust, a professional address |
| 4 | **CI/CD** | Every push to GitHub builds, pushes and deploys automatically | GitHub Actions → `docker build` → push to ECR → update the ECS service | Manual deployment doesn't scale and is error-prone |
| 5 | **Secrets Manager** | Encrypted, access-controlled storage for keys and passwords | AWS Secrets Manager, SSM Parameter Store | Plain env vars in a task definition are readable by anyone with ECS access; secrets can be rotated |
| 6 | **Infrastructure as Code** | Describe ECS, ALB, ECR and security groups in code instead of clicking | Terraform (`.tf` files); AWS-native options: CloudFormation, CDK | Repeatable, reviewable, rebuild or delete everything with one command |
| 7 | **Kubernetes / EKS** | A more powerful (and more complex) container orchestrator | Pods, Deployments, Services, Ingress, ConfigMaps, Helm | The standard in large MLOps and microservice platforms |
| 8 | **Safe releases** | Ship new versions with no downtime and quick rollback | Rolling updates (ECS default), blue/green (CodeDeploy) | A bad release shouldn't take the app down |
| 9 | **Cost optimisation** | Spend only on what's needed | Right-size CPU/memory, scale to zero or delete idle resources, check Cost Explorer | Cloud engineering is also cost engineering. See [04_aws_cleanup_and_costs.md](04_aws_cleanup_and_costs.md) |
| 10 | **Security** | Defence in depth | Least-privilege IAM, private subnets, WAF, security group chains, VPC design | Production must be secure, not just working |

## How they map onto this deployment

| What the lab did | Production version | Topic |
|---|---|---|
| IAM user with AdministratorAccess + access key | Least-privilege role; short-lived credentials (SSO, or GitHub OIDC for CI) | 4, 10 |
| API key as a plain env var | Secrets Manager reference in the task definition | 5 |
| `http://` ALB DNS name | Route 53 domain + ACM certificate + HTTPS listener | 3 |
| Port 8000 open to the internet | Task security group only accepts the ALB's security group; tasks in private subnets | 10 |
| Desired count fixed at 1 | Auto scaling between, say, 1 and 4 tasks | 2 |
| `docker push :latest` by hand | CI pipeline pushing a tag per commit, then a rolling deploy | 4, 8 |
| Console clicking | Terraform or CDK | 6 |
| Output files written inside the container | S3 (container storage disappears on restart) | — |

## Additions not in the session's list

- **Asynchronous processing for long jobs.** LLM pipelines over big files can outlast HTTP timeouts (see the ALB note in [02](02_deploying_on_aws_ecs_fargate.md)). The production pattern:
  1. Upload the file to S3.
  2. Put a job on a queue (SQS).
  3. A worker processes it.
  4. The client polls or gets notified when the result is ready.
- **LLM-specific observability.** Beyond CPU and memory, track token usage, cost per request, latency per LLM call and failure rates. Tracing tools like LangSmith or Langfuse show each step of the chain.
- **Rate limits and retries.** LLM APIs throttle. Retries with backoff and a cap on parallel calls keep a busy app from failing in bursts.

## A sensible order to learn them

For a GenAI app like this one:

1. **Secrets Manager.** Small change, big security gain.
2. **CloudWatch logs and alarms.** You can't fix what you can't see.
3. **CI/CD with GitHub Actions.** It stops the manual build-tag-push routine.
4. **Domain + HTTPS.**
5. **Terraform or CDK.** Rebuild this whole stack from code.
6. **Auto scaling, then EKS** if you go deeper into MLOps.

> **Takeaway:** deploying an app proves it runs. Engineering a production system means it deploys itself, scales itself, keeps its secrets, tells you when it's sick, and doesn't waste money.

## Check yourself

1. Which two changes would most improve the security of this lab deployment, and why?
2. Sketch the CI/CD steps from `git push` to a new task running in ECS.
3. What problem does Terraform solve that the AWS console doesn't?
4. Why might an LLM pipeline need a queue even if a single request is fast?
