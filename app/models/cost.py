from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class CostEntry(Base):
    __tablename__ = "cost_entries"

    id            = Column(Integer, primary_key=True, index=True)
    amount_usd    = Column(Float, nullable=False)
    recorded_date = Column(Date, nullable=False)
    description   = Column(String, nullable=True)
    created_at    = Column(DateTime, default=datetime.now)

    resource_id   = Column(Integer, ForeignKey("resources.id"))
    resource      = relationship("Resource", back_populates="cost_entries")