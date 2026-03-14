from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CostCreate(BaseModel):
    resource_id: int
    amount_usd: float
    recorded_date: date
    description: Optional[str] = None

class CostResponse(BaseModel):
    id: int
    resource_id: int
    amount_usd: float
    recorded_date: date
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True