from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from webhook import service
from webhook.schemas import WebhookCreate, WebhookResponse, WebhookUpdate

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
def create_webhook(data: WebhookCreate, db: Session = Depends(get_db)):
    return service.create_webhook(db, data)


@router.get("", response_model=list[WebhookResponse])
def get_all_webhooks(db: Session = Depends(get_db)):
    return service.get_all_webhooks(db)


@router.get("/{webhook_id}", response_model=WebhookResponse)
def get_webhook(webhook_id: str, db: Session = Depends(get_db)):
    return service.get_webhook(db, webhook_id)


@router.patch("/{webhook_id}", response_model=WebhookResponse)
def update_webhook(webhook_id: str, data: WebhookUpdate, db: Session = Depends(get_db)):
    return service.update_webhook(db, webhook_id, data)


@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: str, db: Session = Depends(get_db)):
    service.delete_webhook(db, webhook_id)
    return {"message": "Webhook deleted"}