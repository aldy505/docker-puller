from pydantic import BaseModel


class PullResponse(BaseModel):
    queued: bool
