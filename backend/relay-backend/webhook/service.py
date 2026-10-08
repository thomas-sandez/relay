import uuid

from fastapi import HTTPException

from webhook.schemas import WebhookCreate, WebhookResponse, WebhookUpdate

_webhooks: dict[str, WebhookResponse] = {}


def create_webhook(data: WebhookCreate) -> WebhookResponse:
    webhook = WebhookResponse(
        id=f"webhook_{uuid.uuid4().hex[:8]}",
        name=data.name,
        url=str(data.url),
        maxRetries=data.maxRetries,
        timeoutSeconds=data.timeoutSeconds,
        active=True,
    )
    _webhooks[webhook.id] = webhook
    return webhook


def get_all_webhooks() -> list[WebhookResponse]:
    return list(_webhooks.values())


def get_webhook(webhook_id: str) -> WebhookResponse:
    webhook = _webhooks.get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook


def update_webhook(webhook_id: str, data: WebhookUpdate) -> WebhookResponse:
    webhook = get_webhook(webhook_id)
    changes = data.model_dump(exclude_unset=True)
    if "url" in changes and changes["url"] is not None:
        changes["url"] = str(changes["url"])
    updated = webhook.model_copy(update=changes)
    _webhooks[webhook_id] = updated
    return updated


def delete_webhook(webhook_id: str) -> None:
    get_webhook(webhook_id)
    del _webhooks[webhook_id]
