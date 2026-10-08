from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from webhook.models import Webhook
from events.models import Event, EventStatus
from events.schemas import EventIngestRequest, EventIngestResponse

router = APIRouter(prefix="/api/webhooks", tags=["Events"])

@router.post(
    "/{webhook_id}/events",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=EventIngestResponse
)
def ingest_event(
    webhook_id: str,
    body: EventIngestRequest,
    db: Session = Depends(get_db)
):
    # 1. Validar webhook y estado activo
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Webhook with id '{webhook_id}' not found"
        )
    if not webhook.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook is currently disabled"
        )

    # 2. Persistir evento en base de datos
    new_event = Event(
        webhook_id=webhook.id,
        event_type=body.eventType,
        payload=body.payload,
        status=EventStatus.RECEIVED
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # TODO (Milestone 4): Publicar new_event.id en RabbitMQ

    return EventIngestResponse(
        eventId=new_event.id,
        status=new_event.status,
        createdAt=new_event.created_at
    )