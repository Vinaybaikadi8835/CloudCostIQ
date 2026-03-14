from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=data.email, password=data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user