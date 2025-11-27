from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    title: str
    duration_quarters: int = Field(gt=0)
    price: Decimal = Field(gt=0)
    master_id: int


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    duration_quarters: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)
    master_id: Optional[int] = None


class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True


class ServiceListResponse(BaseModel):
    id: int
    title: str
    price: Decimal
    duration_quarters: int
    master_id: int
    master_full_name: str
    master_role: str
    master_phone_number: str

    class Config:
        from_attributes = True


class FreeQuartersResponse(BaseModel):
    free_quarters: list[int]

