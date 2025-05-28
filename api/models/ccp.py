from api.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from datetime import datetime
from sqlalchemy.orm import relationship


class CCPCategories(Base):
    __tablename__ = "ccp_categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    is_violation = Column(Boolean, default=False)
    points = Column(Integer, default=0)
    


class CCPLog(Base):
    __tablename__ = "ccp_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("users.id"), index=True)
    category_id = Column(Integer, ForeignKey("ccp_categories.id"), index=True)
    date_logged = Column(DateTime, default=datetime.now)
    points_awarded = Column(Integer, default=0)
    notes = Column(String(255))

    category = relationship("CCPCategories", backref="logs")
