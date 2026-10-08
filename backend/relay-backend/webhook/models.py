import uuid

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True, default=lambda: f"webhook_{uuid.uuid4().hex[:8]}")
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    max_retries = Column(Integer, nullable=False, default=5)
    timeout_seconds = Column(Integer, nullable=False, default=10)
    active = Column(Boolean, nullable=False, default=True)

    events = relationship("Event", back_populates="webhook", cascade="all, delete-orphan")
