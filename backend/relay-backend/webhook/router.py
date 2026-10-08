from fastapi import APIRouter, status

from webhook import service
from webhook.schemas import WebhookCreate, WebhookResponse

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
def create_webhook(data: WebhookCreate):
    return service.create_webhook(data)
