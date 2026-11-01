# Live session · Shutting down AWS resources and avoiding surprise bills

Cloud resources keep charging until you delete them, whether or not anyone uses the app. The session's checklist, with the reasoning and a few gaps filled in.

## What actually costs money

| Resource | Billed? | How |
|---|---|---|
| **ECS on Fargate** | ✅ | Per second, for the vCPU and memory of every **running task** |
| **Application Load Balancer** | ✅ | Per hour it **exists**, plus traffic units, even with zero traffic |
| **Public IPv4 addresses** | ✅ | Per hour, per address (since February 2024). The task's public IP and each ALB node's IP count. *Missing from the session's table* |
| **ECR** | ✅ (small) | Per GB stored per month; a single image costs cents |
| **CloudWatch Logs** | ⚠️ small | Per GB ingested and stored |
| IAM users and roles | ❌ | Free |
| Security groups | ❌ | Free |
| ECS cluster (empty) | ❌ | Free; you pay for the tasks, not the cluster |

Rough scale in `us-east-1` at list prices (check the AWS pricing pages for current numbers):

- one small Fargate task running 24/7 costs tens of dollars a month;
- an idle ALB costs roughly $15–20 a month;
- each public IPv4 address costs about $3.60 a month.

A forgotten lab deployment can easily cost **$50+ a month**.

## The cleanup order

The order matters because resources depend on each other. You can't delete a target group while a load balancer or service still uses it.

| # | Delete | Where | Note |
|---|---|---|---|
| 1 | **ECS service** | ECS → cluster → Services → Delete | Set the desired count to 0 first, or use force delete. This stops the Fargate billing |
| 2 | Any **running tasks** | ECS → cluster → Tasks → Stop | Check that the list is empty |
| 3 | **ECS cluster** | ECS → Clusters → Delete | |
| 4 | **Application Load Balancer** | EC2 → Load balancers → Delete | ⚠️ Keeps billing until deleted |
| 5 | **Target group** | EC2 → Target groups → Delete | Only possible once the ALB is gone |
| 6 | **ECR repository** | ECR → Repositories → Delete | Type "delete" to force it if images remain |
| 7 | CloudWatch log groups (optional) | CloudWatch → Log groups | Usually `/ecs/AI-qa-evaluator-task` |
| 8 | Custom security groups (optional) | EC2 → Security groups | Only ones **you** created, e.g. `qa-evaluator-sg`. **Never delete the VPC's `default` group** |
| 9 | IAM user (optional) | IAM → Users | If it was only for this lab. At the very least, **deactivate or delete its access key** |

The same steps from the CLI (names from the guide):

```bash
aws ecs update-service --cluster qa-evaluator-cluster --service qa-evaluator-service --desired-count 0
aws ecs delete-service --cluster qa-evaluator-cluster --service qa-evaluator-service --force
aws ecs delete-cluster --cluster qa-evaluator-cluster
aws elbv2 delete-load-balancer --load-balancer-arn <alb-arn>
aws elbv2 delete-target-group --target-group-arn <tg-arn>
aws ecr delete-repository --repository-name qa-evaluator-app --force
```

## Pause instead of delete

If you'll come back to it soon:

```bash
aws ecs update-service --cluster qa-evaluator-cluster --service qa-evaluator-service --desired-count 0
```

This stops the Fargate and task-IP charges. Set it back to 1 to resume. The task definition, the image and the service settings are all kept. **The ALB still bills while it exists**, so delete it if the pause will be long, and recreate it later (phase 6 of the [AWS notes](02_deploying_on_aws_ecs_fargate.md)).

## Habits that prevent surprise bills

- **Set a budget alert:** AWS Billing → Budgets → a monthly cost budget with an email alert at a few dollars.
- **Check after a lab:** ECS → Clusters should show no running tasks, and EC2 → Load balancers should be empty.
- **Look at Cost Explorer** a day later. Charges appear with a delay, so a quiet bill on day one proves nothing.
- On **Azure**, deleting the resource group removes everything at once. On **GCP**, delete the Cloud Run service and Artifact Registry repository, or the whole project if it was only for the lab.

> **Takeaway:** in AWS you pay for what **exists**, not for what's used. Delete the service (or scale it to 0) and the load balancer first; they're the expensive parts. Free resources like IAM roles and security groups can wait.

## Check yourself

1. Which two resources in this project keep costing money even when nobody uses the app?
2. Why must the ALB be deleted before its target group?
3. What does scaling the service to 0 stop, and what keeps billing?
4. Which security group must you never delete?
