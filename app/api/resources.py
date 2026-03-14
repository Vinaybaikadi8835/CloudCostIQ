from fastapi import APIRouter, HTTPException
from app.schemas.resource import ResourceCreate, ResourceResponse
from datetime import datetime
from typing import List

router = APIRouter()

# Temporary storage — like a whiteboard, resets when server restarts
# We replace this with real PostgreSQL in Step 3
fake_db = []
counter = 1

@router.get("/", response_model=List[ResourceResponse])
def get_all_resources():
    """Get all cloud resources"""
    return fake_db

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int):
    """Get a single resource by ID"""
    for resource in fake_db:
        if resource["id"] == resource_id:
            return resource
    raise HTTPException(status_code=404, detail="Resource not found")

@router.post("/", response_model=ResourceResponse, status_code=201)
def create_resource(data: ResourceCreate):
    """Create a new cloud resource"""
    global counter
    new_resource = {
        "id": counter,
        "name": data.name,
        "provider": data.provider,
        "resource_type": data.resource_type,
        "region": data.region,
        "created_at": datetime.now()
    }
    fake_db.append(new_resource)
    counter += 1
    return new_resource

@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, data: ResourceCreate):
    """Update an existing resource"""
    for index, resource in enumerate(fake_db):
        if resource["id"] == resource_id:
            fake_db[index].update({
                "name": data.name,
                "provider": data.provider,
                "resource_type": data.resource_type,
                "region": data.region
            })
            return fake_db[index]
    raise HTTPException(status_code=404, detail="Resource not found")

@router.delete("/{resource_id}")
def delete_resource(resource_id: int):
    """Delete a resource"""
    global fake_db
    original_length = len(fake_db)
    fake_db = [r for r in fake_db if r["id"] != resource_id]
    if len(fake_db) == original_length:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": f"Resource {resource_id} deleted successfully"}