from api.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from uuid import uuid4
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
