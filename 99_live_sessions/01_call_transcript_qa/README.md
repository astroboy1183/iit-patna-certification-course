# Live session 01 · Call-transcript classification and QA evaluation

Built during the program's Sunday live session. A LangChain pipeline over customer-support call transcripts:

1. **Classify** each call as `billing`, `claims`, `complaint` or `general_query` (Pydantic-validated output with a confidence score).
2. **Route** each call to the evaluations that matter for its type.
3. **Score** tone and empathy, resolution quality and knowledge accuracy (1–5, with a justification), each with its own prompt and parser.

| File | Purpose |
|---|---|
| [experiment.ipynb](experiment.ipynb) | The pipeline, built step by step |
| [config/config.json](config/config.json) | Models, temperature, evaluation criteria, classification labels |
| [data/](data) | Sample call transcripts |
| [src/](src) | The pipeline as modules; [src/pipeline/inference.py](src/pipeline/inference.py) runs it end to end |
| [main.py](main.py) | Command-line entry point |
| [app.py](app.py) | FastAPI app: upload a transcripts file to `/evaluate`, get the results back as Excel |
| [Dockerfile](Dockerfile), [.dockerignore](.dockerignore) | Runs the FastAPI app in a container |

Run it with the venv in this folder (`pip install -r requirements.txt`) and `OPENAI_API_KEY` or `GEMINI_API_KEY` plus `LLM_PROVIDER` in a `.env` file.

## Three ways to run it

```bash
python main.py                                        # every transcript -> data/output.xlsx
uvicorn app:app --reload                              # API on http://localhost:8000/docs

docker build -t qa-evaluator .                        # API in a container
docker run --env-file .env -p 8000:8000 qa-evaluator  # also http://localhost:8000/docs
```

`.env` is listed in `.dockerignore`, so the API keys never go into the image; `--env-file` passes them in when the container starts.

## How a request reaches the app

**Without Docker.** uvicorn runs on the laptop and listens on port 8000. The browser connects from a temporary port of its own (e.g. 54321) and sends the request to port 8000. uvicorn hands it to FastAPI, which runs the pipeline, and the response goes back over the same connection to the browser's port, not to port 8000.

```
browser (laptop:54321)  ⇄  uvicorn (laptop:8000)  →  FastAPI
```

**With Docker.** The container is an isolated mini-machine with its own Python, packages, files and network, so it has its own port 8000. uvicorn listens there (the `--port 8000` in the Dockerfile's `CMD`). The browser can't see inside the container, so `-p 8000:8000` tells Docker to listen on the laptop's port 8000 and forward traffic into the container:

```
browser (laptop:54321)  ⇄  Docker (laptop:8000)                  connection 1
Docker (172.17.0.1:62688)  ⇄  uvicorn (container:8000)  →  FastAPI   connection 2
```

The response travels back along connection 2 to Docker, and Docker passes it along connection 1 to the browser. The browser only ever sees `localhost:8000`. That's also why the container's log shows requests coming from `172.17.0.1`, Docker's address, rather than from the browser.

In `-p 8000:8000`, the left number is the laptop's port and the right one is the container's:

- The container's port never clashes with anything on the laptop.
- The laptop's port must be free. If `uvicorn app:app` is still running locally, `docker run` fails with `bind: address already in use`. Stop uvicorn (Ctrl+C), or map a different laptop port with `-p 8001:8000` and open `localhost:8001/docs`.
- Without `-p` the container still runs, but nothing on the laptop can reach it.

## Notes: deploying it (live session)

| # | Topic |
|---|---|
| 1 | [Deployment architectures](notes/01_deployment_architectures.md): EC2 vs ECS + Fargate vs Lambda, and why containers fit this app |
| 2 | [Deploying on AWS](notes/02_deploying_on_aws_ecs_fargate.md): Docker → ECR → ECS + Fargate → ALB, the API key, new releases, troubleshooting |
| 3 | [The same on Azure and GCP](notes/03_deploying_on_azure_and_gcp.md): Container Apps + ACR, Cloud Run + Artifact Registry |
| 4 | [AWS cleanup and costs](notes/04_aws_cleanup_and_costs.md): what bills, the deletion order, pausing |
| 5 | [After deployment](notes/05_after_deployment_roadmap.md): monitoring, scaling, HTTPS, CI/CD, secrets, IaC |

The notes follow the session's guides and mark where I've corrected or added to them.
