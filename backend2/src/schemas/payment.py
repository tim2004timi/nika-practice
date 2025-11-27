from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    appointment_id: int
    amount: Decimal = Field(gt=0)


class PaymentResponse(BaseModel):
    date: date
    time: str
    service_title: str
    client_full_name: str
    amount: Decimal

    class Config:
        from_attributes = True

