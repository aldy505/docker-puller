from pydantic import BaseModel


class PullRequest(BaseModel):
    image_repository: str
    image_tag: str
    image_digest: str
    container_name: str
