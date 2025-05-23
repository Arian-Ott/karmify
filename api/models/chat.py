from api.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from api.models.users import UserTable
from datetime import datetime


class DMTable(Base):
    __tablename__ = "dm_chats"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
class DMMessageTable(Base):
    __tablename__ = "dm_messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("dm_chats.id"), index=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    content = Column(String(1024))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    