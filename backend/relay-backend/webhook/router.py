from fastapi import APIRouter, status

from webhook import service
from webhook.schemas import WebhookCreate, WebhookResponse, WebhookUpdate

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
def create_webhook(data: WebhookCreate):
    return service.create_webhook(data)


@router.get("", response_model=list[WebhookResponse])
def get_all_webhooks():
    return service.get_all_webhooks()


@router.get("/{webhook_id}", response_model=WebhookResponse)
def get_webhook(webhook_id: str):
    return service.get_webhook(webhook_id)


@router.patch("/{webhook_id}", response_model=WebhookResponse)
def update_webhook(webhook_id: str, data: WebhookUpdate):
    return service.update_webhook(webhook_id, data)


@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: str):
    service.delete_webhook(webhook_id)
    return {"message": "Webhook deleted"}