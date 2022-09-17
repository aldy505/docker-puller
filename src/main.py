import os
import docker
from docker.errors import APIError
from fastapi import FastAPI, status, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from error_response import ErrorResponse
from health_response import HealthResponse
from pull_request import PullRequest
from pull_response import PullResponse
from pull_task import pull_task

access_token = os.getenv("TOKEN")
configuration_path = os.getenv("CONFIGURATION_PATH")
environment = os.getenv("ENVIRONMENT")
docker_client = docker.from_env()

openapi_url = "/openapi.json"
if environment is not None and environment == "production":
    openapi_url = None

if access_token is None:
    print("TOKEN environment variable must not be empty")
    exit(1)

if configuration_path is None:
    configuration_path = "conf/"

app = FastAPI(
    title="Docker Puller",
    redoc_url=None,
    openapi_url=openapi_url,
    version="0.0.1",
    contact={
        "name": "Reinaldy Rafli",
        "url": "https://github.com/aldy505",
        "email": "aldy505@proton.me",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    on_shutdown=docker_client.close()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[],
)


@app.get("/health", response_model=HealthResponse)
def health_controller(token: str | None = Header(default=None)):
    if token is None or token == "":
        error_message = ErrorResponse(message="empty token")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_message.dict())

    if token != access_token:
        error_message = ErrorResponse(message="invalid token")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_message.dict())

    try:
        docker_version = docker_client.version()

        docker_ping = docker_client.ping()

        response = HealthResponse(docker_ok=docker_ping, docker_version=docker_version["Version"])

        if not docker_ping:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.dict())

        return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict())
    except APIError as e:
        error_message = ErrorResponse(message="docker error: " + e.response)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message.dict())


@app.post("/pull", response_model=PullResponse)
def pull_controller(body_payload: PullRequest, background_tasks: BackgroundTasks,
                    token: str | None = Header(default=None)):
    if token is None or token == "":
        error_message = ErrorResponse(message="empty token")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_message.dict())

    if token != access_token:
        error_message = ErrorResponse(message="invalid token")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_message.dict())

    if body_payload.image_repository == "" or body_payload.image_digest == "":
        error_message = ErrorResponse(message="payload body is empty string")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message.dict())

    background_tasks.add_task(pull_task, docker_client, configuration_path, body_payload)
    response = PullResponse(queued=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
