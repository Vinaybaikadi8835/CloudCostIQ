from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models.cost import CostEntry
from app.models.resource import Resource
from app.schemas.cost import CostCreate, CostResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CostResponse])
def get_all_costs(db: Session = Depends(get_db)):
    return db.query(CostEntry).all()

@router.get("/summary")
def get_cost_summary(db: Session = Depends(get_db)):
    results = (
        db.query(Resource.provider, func.sum(CostEntry.amount_usd).label("total"))
        .join(CostEntry, CostEntry.resource_id == Resource.id)
        .group_by(Resource.provider)
        .all()
    )
    summary = {row.provider: round(row.total, 2) for row in results}
    return {"summary": summary, "total": round(sum(summary.values()), 2)}

@router.post("/", response_model=CostResponse, status_code=201)
def create_cost_entry(data: CostCreate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == data.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    new_cost = CostEntry(
        resource_id=data.resource_id,
        amount_usd=data.amount_usd,
        recorded_date=data.recorded_date,
        description=data.description
    )
    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)
    return new_cost

@router.delete("/{cost_id}")
def delete_cost(cost_id: int, db: Session = Depends(get_db)):
    cost = db.query(CostEntry).filter(CostEntry.id == cost_id).first()
    if not cost:
        raise HTTPException(status_code=404, detail="Cost entry not found")
    db.delete(cost)
    db.commit()
    return {"message": f"Cost {cost_id} deleted"}