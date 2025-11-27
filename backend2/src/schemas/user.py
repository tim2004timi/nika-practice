from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    login: str
    full_name: str
    phone_number: str
    role: str = Field(default="CLIENT", pattern="^(CLIENT|VIZAZHIST|MANICURIST|STYLIST|BROWIST)$")


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MasterResponse(BaseModel):
    id: int
    full_name: str
    role: str
    phone_number: str
    services_count: int

    class Config:
        from_attributes = True

