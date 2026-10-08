from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict
from datetime import datetime
from events.models import EventStatus

class EventIngestRequest(BaseModel):
    eventType: str = Field(..., min_length=1, max_length=100, example="order.created")
    payload: Dict[str, Any] = Field(..., example={"orderId": 123, "customerId": 456})

class EventIngestResponse(BaseModel):
    eventId: str
    status: EventStatus
    createdAt: datetime

    model_config = ConfigDict(from_attributes=True)