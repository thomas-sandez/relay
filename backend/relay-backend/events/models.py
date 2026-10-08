import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from database import Base

class EventStatus(str, enum.Enum):
    RECEIVED = "RECEIVED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DLQ = "DLQ"

class Event(Base):
    __tablename__ = "events"

    # Prefijo legible o UUID estándar
    id = Column(String, primary_key=True, default=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    webhook_id = Column(String, ForeignKey("webhooks.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.RECEIVED, nullable=False)
    attempt_count = Column(Integer, default=0, nullable=False)
    last_error = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    # Relación opcional si querés navegar desde el webhook
    webhook = relationship("Webhook", back_populates="events")