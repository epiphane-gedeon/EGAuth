from sqlalchemy import (
    Column, Integer, String, Text, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    token_version = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

