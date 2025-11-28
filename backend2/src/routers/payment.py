from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth import get_current_user
from src.models.user import User
from src.schemas.payment import PaymentCreate, PaymentResponse
from src.crud.payment import get_payments_by_master, create_payment, quarter_to_time
from src.crud.appointment import get_appointment_by_id
from src.crud.service import get_service_by_id
from src.crud.user import get_user_by_id

router = APIRouter(prefix="/payments")


@router.get("/me", response_model=list[PaymentResponse])
async def get_my_payments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение списка оплат для текущего мастера"""
    payments = await get_payments_by_master(db, current_user.id)
    return [PaymentResponse(**payment) for payment in payments]


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment_endpoint(
    payment_create: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создание новой оплаты"""
    # Проверяем, существует ли запись
    appointment = await get_appointment_by_id(db, payment_create.appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Создаем оплату
    payment = await create_payment(db, payment_create)
    
    # Получаем полную информацию для ответа
    service = await get_service_by_id(db, appointment.service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    client = await get_user_by_id(db, appointment.client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Преобразуем quarter в время
    time_str = quarter_to_time(appointment.quarter)
    
    return PaymentResponse(
        date=appointment.date,
        time=time_str,
        service_title=service.title,
        client_full_name=client.full_name,
        amount=payment.amount
    )

