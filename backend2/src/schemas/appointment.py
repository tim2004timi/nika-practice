from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    client_id: int
    service_id: int
    date: date
    quarter: int = Field(ge=1, le=20)
    status: str = Field(default="booked", pattern="^(booked|in_progress|completed)$")
    is_paid: bool = False


class AppointmentListResponse(BaseModel):
    id: int
    date: date
    quarter: int
    status: str
    is_paid: bool
    master_full_name: str
    service_title: str
    service_price: Decimal
    client_full_name: str

    class Config:
        from_attributes = True


class AppointmentDetailResponse(AppointmentListResponse):
    pass


class AppointmentUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(booked|in_progress|completed)$")
    is_paid: Optional[bool] = None

