from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from src.models.payment import Payment
from src.models.appointment import Appointment
from src.models.service import Service
from src.models.user import User
from src.schemas.payment import PaymentCreate
from src.crud.service import get_service_by_id
from src.crud.user import get_user_by_id
from src.crud.appointment import get_appointment_by_id


def quarter_to_time(quarter: int) -> str:
    """Преобразует квартал в время в формате HH:MM"""
    # Quarter 1 = 8:00, quarter 2 = 8:30, и т.д.
    hours = 8
    minutes = (quarter - 1) * 30
    hours += minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"


async def get_payments_by_master(
    db: AsyncSession,
    master_id: int
) -> List[dict]:
    """
    Получает все оплаты для мастера через его записи.
    
    Returns:
        Список словарей с данными оплат
    """
    # Получаем все записи мастера через услуги
    result = await db.execute(
        select(Appointment)
        .join(Service, Appointment.service_id == Service.id)
        .where(Service.master_id == master_id)
    )
    appointments = list(result.scalars().all())
    
    # Получаем все оплаты для этих записей
    appointment_ids = [app.id for app in appointments]
    if not appointment_ids:
        return []
    
    payments_result = await db.execute(
        select(Payment).where(Payment.appointment_id.in_(appointment_ids))
    )
    payments = list(payments_result.scalars().all())
    
    # Формируем ответ с полной информацией
    result_list = []
    for payment in payments:
        # Находим запись для этого платежа
        appointment = next((a for a in appointments if a.id == payment.appointment_id), None)
        if not appointment:
            continue
        
        # Получаем услугу
        service = await get_service_by_id(db, appointment.service_id)
        if not service:
            continue
        
        # Получаем клиента
        client = await get_user_by_id(db, appointment.client_id)
        if not client:
            continue
        
        # Преобразуем quarter в время
        time_str = quarter_to_time(appointment.quarter)
        
        result_list.append({
            "date": appointment.date,
            "time": time_str,
            "service_title": service.title,
            "client_full_name": client.full_name,
            "amount": payment.amount
        })
    
    return result_list


async def create_payment(
    db: AsyncSession,
    payment_create: PaymentCreate
) -> Payment:
    """Создает новую оплату"""
    db_payment = Payment(
        appointment_id=payment_create.appointment_id,
        amount=payment_create.amount
    )
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

