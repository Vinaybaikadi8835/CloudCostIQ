from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr      # Pydantic validates this is a real email format
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True