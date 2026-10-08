from pydantic import BaseModel, HttpUrl, Field


class WebhookCreate(BaseModel):
    name: str
    url: HttpUrl
    maxRetries: int = Field(default=5, ge=0)
    timeoutSeconds: int = Field(default=10, gt=0)


class WebhookResponse(BaseModel):
    id: str
    name: str
    url: str
    maxRetries: int
    timeoutSeconds: int
    active: bool
