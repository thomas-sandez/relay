from fastapi import HTTPException
from sqlalchemy.orm import Session

from webhook.models import Webhook
from webhook.schemas import WebhookCreate, WebhookResponse, WebhookUpdate


def _to_response(webhook: Webhook) -> WebhookResponse:
    return WebhookResponse(
        id=webhook.id,
        name=webhook.name,
        url=webhook.url,
        maxRetries=webhook.max_retries,
        timeoutSeconds=webhook.timeout_seconds,
        active=webhook.active,
    )


def _get_or_404(db: Session, webhook_id: str) -> Webhook:
    webhook = db.get(Webhook, webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook


def create_webhook(db: Session, data: WebhookCreate) -> WebhookResponse:
    webhook = Webhook(
        name=data.name,
        url=str(data.url),
        max_retries=data.maxRetries,
        timeout_seconds=data.timeoutSeconds,
        active=True,
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return _to_response(webhook)


def get_all_webhooks(db: Session) -> list[WebhookResponse]:
    return [_to_response(w) for w in db.query(Webhook).all()]


def get_webhook(db: Session, webhook_id: str) -> WebhookResponse:
    return _to_response(_get_or_404(db, webhook_id))


def update_webhook(db: Session, webhook_id: str, data: WebhookUpdate) -> WebhookResponse:
    webhook = _get_or_404(db, webhook_id)
    changes = data.model_dump(exclude_unset=True)
    mapping = {"maxRetries": "max_retries", "timeoutSeconds": "timeout_seconds"}
    for key, value in changes.items():
        if value is None:
            continue
        if key == "url":
            value = str(value)
        setattr(webhook, mapping.get(key, key), value)
    db.commit()
    db.refresh(webhook)
    return _to_response(webhook)


def delete_webhook(db: Session, webhook_id: str) -> None:
    webhook = _get_or_404(db, webhook_id)
    db.delete(webhook)
    db.commit()
