from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from typing import List

router = APIRouter()

fake_users = []
user_counter = 1

@router.get("/", response_model=List[UserResponse])
def get_all_users():
    return fake_users

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate):
    global user_counter
    # Check if email already exists
    for user in fake_users:
        if user["email"] == data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    new_user = {
        "id": user_counter,
        "email": data.email,
        # Never store plain passwords — we add hashing in Step 4
        "password": data.password
    }
    fake_users.append(new_user)
    user_counter += 1
    return new_user