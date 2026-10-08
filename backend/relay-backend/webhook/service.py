import uuid

from webhook.schemas import WebhookCreate, WebhookResponse

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
