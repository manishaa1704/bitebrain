from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for registering a new user"""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Schema for logging in"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for returning user data (never includes password)"""
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    """Schema for returning JWT token"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for data stored inside JWT token"""
    user_id: int | None = None