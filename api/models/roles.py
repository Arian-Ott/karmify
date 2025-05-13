from api.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from api.models.users import UserTable
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import relationship


class RoleTable(Base):
    __tablename__ = "roles"
    name = Column(String(50), primary_key=True, index=True)
    description = Column(String(255))


class UserRoleTable(Base):
    __tablename__ = "user_roles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_name = Column(String(50), ForeignKey("roles.name"), primary_key=True)
    date_assigned = Column(DateTime, default=datetime.now)
