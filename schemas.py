from pydantic import BaseModel
from typing import List, Optional

# --- Auth Schemas ---
class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "violator"

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Excuse Schemas ---
class ExcuseCreate(BaseModel):
    text: str
    category: str

class ExcuseResponse(BaseModel):
    id: int
    text: str
    category: str
    rating: int
    class Config:
        from_attributes = True

# --- Violation Schemas ---
class ViolationCreate(BaseModel):
    title: str
    description: str
    employee_id: int

class ViolationResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    employee_id: int
    excuses: List[ExcuseResponse] = []
    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: str
