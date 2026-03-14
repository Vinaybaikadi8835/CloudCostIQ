from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ResourceResponse])
def get_all_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.post("/", response_model=ResourceResponse, status_code=201)
def create_resource(data: ResourceCreate, db: Session = Depends(get_db)):
    new_resource = Resource(
        name=data.name,
        provider=data.provider,
        resource_type=data.resource_type,
        region=data.region
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, data: ResourceCreate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource.name          = data.name
    resource.provider      = data.provider
    resource.resource_type = data.resource_type
    resource.region        = data.region
    db.commit()
    db.refresh(resource)
    return resource

@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    return {"message": f"Resource {resource_id} deleted"}