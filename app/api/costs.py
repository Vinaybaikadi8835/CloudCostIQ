from fastapi import APIRouter, HTTPException
from app.schemas.cost import CostCreate, CostResponse
from datetime import datetime
from typing import List

router = APIRouter()

fake_costs = []
cost_counter = 1

@router.get("/", response_model=List[CostResponse])
def get_all_costs():
    """Get all cost entries"""
    return fake_costs

@router.get("/summary")
def get_cost_summary():
    """Get total cost grouped by provider"""
    summary = {}
    for cost in fake_costs:
        provider = cost.get("provider", "unknown")
        summary[provider] = summary.get(provider, 0) + cost["amount_usd"]
    return {"summary": summary, "total": sum(summary.values())}

@router.post("/", response_model=CostResponse, status_code=201)
def create_cost_entry(data: CostCreate):
    """Log a new cost entry"""
    global cost_counter
    new_cost = {
        "id": cost_counter,
        "resource_id": data.resource_id,
        "amount_usd": data.amount_usd,
        "recorded_date": data.recorded_date,
        "description": data.description,
        "created_at": datetime.now()
    }
    fake_costs.append(new_cost)
    cost_counter += 1
    return new_cost

@router.delete("/{cost_id}")
def delete_cost(cost_id: int):
    """Delete a cost entry"""
    global fake_costs
    original = len(fake_costs)
    fake_costs = [c for c in fake_costs if c["id"] != cost_id]
    if len(fake_costs) == original:
        raise HTTPException(status_code=404, detail="Cost entry not found")
    return {"message": f"Cost {cost_id} deleted"}