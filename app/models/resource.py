from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Resource(Base):
    __tablename__ = "resources"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    provider      = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    region        = Column(String, nullable=True)
    created_at    = Column(DateTime, default=datetime.now)

    owner_id      = Column(Integer, ForeignKey("users.id"))
    owner         = relationship("User", back_populates="resources")
    cost_entries  = relationship("CostEntry", back_populates="resource")