from pydantic import BaseModel


class HealthResponse(BaseModel):
    docker_ok: bool
    docker_version: str
