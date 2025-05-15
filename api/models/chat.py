from api.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from api.models.users import UserTable
from datetime import datetime


class ChatTable(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ChatUserTable(Base):
    __tablename__ = "chat_users"
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

    date_joined = Column(DateTime, default=datetime.now)


class MessageTable(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False, index=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
