from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# What data we ACCEPT when creating a resource
class ResourceCreate(BaseModel):
    name: str
    provider: str        # "aws", "azure", "gcp"
    resource_type: str   # "ec2", "vm", "s3"
    region: Optional[str] = None

# What data we SEND BACK in responses
class ResourceResponse(BaseModel):
    id: int
    name: str
    provider: str
    resource_type: str
    region: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True