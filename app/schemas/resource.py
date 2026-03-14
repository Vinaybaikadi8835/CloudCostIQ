from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResourceCreate(BaseModel):
    name: str
    provider: str
    resource_type: str
    region: Optional[str] = None

class ResourceResponse(BaseModel):
    id: int
    name: str
    provider: str
    resource_type: str
    region: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True