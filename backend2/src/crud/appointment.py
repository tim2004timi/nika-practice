from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Dict, Tuple
from datetime import date

from src.models.appointment import Appointment
from src.models.user import User
from src.models.service import Service
from src.schemas.appointment import AppointmentCreate
from src.crud.service import get_service_by_id


async def get_all_appointments(db: AsyncSession) -> List[Appointment]:
    """Получает все записи"""
    result = await db.execute(select(Appointment))
    return list(result.scalars().all())


async def get_appointment_by_id(db: AsyncSession, appointment_id: int) -> Optional[Appointment]:
    """Получает запись по ID"""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    return result.scalar_one_or_none()


async def create_appointment(
    db: AsyncSession, 
    appointment_create: AppointmentCreate
) -> Appointment:
    """Создает новую запись"""
    db_appointment = Appointment(
        client_id=appointment_create.client_id,
        service_id=appointment_create.service_id,
        date=appointment_create.date,
        quarter=appointment_create.quarter,
        status=appointment_create.status,
        is_paid=appointment_create.is_paid
    )
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment


async def update_appointment(
    db: AsyncSession,
    appointment_id: int,
    appointment_update: Dict
) -> Optional[Appointment]:
    """Обновляет запись"""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    db_appointment = result.scalar_one_or_none()
    
    if not db_appointment:
        return None
    
    for field, value in appointment_update.items():
        if value is not None:
            setattr(db_appointment, field, value)
    
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment


async def delete_appointment(db: AsyncSession, appointment_id: int) -> bool:
    """Удаляет запись"""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    db_appointment = result.scalar_one_or_none()
    
    if not db_appointment:
        return False
    
    await db.delete(db_appointment)
    await db.commit()
    return True


async def get_appointments_by_client(
    db: AsyncSession, 
    client_id: int
) -> List[Appointment]:
    """Получает все записи клиента"""
    result = await db.execute(
        select(Appointment).where(Appointment.client_id == client_id)
    )
    return list(result.scalars().all())


async def get_appointments_by_master(
    db: AsyncSession,
    master_id: int
) -> List[Appointment]:
    """Получает все записи мастера через услуги"""
    result = await db.execute(
        select(Appointment)
        .join(Service, Appointment.service_id == Service.id)
        .where(Service.master_id == master_id)
    )
    return list(result.scalars().all())


async def get_appointments_by_master_and_date(
    db: AsyncSession,
    master_id: int,
    appointment_date: date
) -> List[Appointment]:
    """Получает все записи мастера на конкретную дату"""
    result = await db.execute(
        select(Appointment)
        .join(Service, Appointment.service_id == Service.id)
        .where(Service.master_id == master_id)
        .where(Appointment.date == appointment_date)
    )
    return list(result.scalars().all())


async def validate_appointment(
    db: AsyncSession,
    service_id: int,
    appointment_date: date,
    quarter: int,
    duration_quarters: int
) -> Tuple[bool, Optional[str]]:
    """
    Валидирует возможность создания записи.
    
    Проверяет:
    1. Что запись не выходит за границы 20 кварталов
    2. Что запись не накладывается на другие записи мастера в этот день
    
    Returns:
        (is_valid, error_message)
    """
    # Получаем услугу для получения master_id
    service = await get_service_by_id(db, service_id)
    if not service:
        return False, "Service not found"
    
    master_id = service.master_id
    
    # Проверка 1: запись не должна выходить за границы 20 кварталов
    end_quarter = quarter + duration_quarters - 1
    if end_quarter > 20:
        return False, f"Appointment exceeds working hours. End quarter {end_quarter} is beyond 20 (17:30)"
    
    # Проверка 2: запись не должна накладываться на другие записи мастера
    existing_appointments = await get_appointments_by_master_and_date(
        db, master_id, appointment_date
    )
    
    new_start = quarter
    new_end = quarter + duration_quarters - 1
    
    for existing_appointment in existing_appointments:
        # Получаем услугу для существующей записи, чтобы узнать её длительность
        existing_service = await get_service_by_id(db, existing_appointment.service_id)
        if not existing_service:
            continue
        
        existing_start = existing_appointment.quarter
        existing_end = existing_appointment.quarter + existing_service.duration_quarters - 1
        
        # Проверяем наложение интервалов
        # Интервалы не должны пересекаться: (new_start > existing_end) OR (new_end < existing_start)
        if not (new_start > existing_end or new_end < existing_start):
            return False, (
                f"Appointment overlaps with existing appointment. "
                f"Master is busy from quarter {existing_start} to {existing_end}"
            )
    
    return True, None


async def get_free_quarters(
    db: AsyncSession,
    service_id: int,
    appointment_date: date
) -> List[int]:
    """
    Получает список свободных кварталов для услуги на указанную дату.
    
    Учитывает все записи мастера на этот день и длительность услуги.
    
    Returns:
        Список свободных кварталов (1-20)
    """
    # Получаем услугу для получения master_id и duration_quarters
    service = await get_service_by_id(db, service_id)
    if not service:
        return []
    
    master_id = service.master_id
    service_duration = service.duration_quarters
    
    # Получаем все записи мастера на эту дату
    existing_appointments = await get_appointments_by_master_and_date(
        db, master_id, appointment_date
    )
    
    # Создаем множество занятых кварталов
    busy_quarters = set()
    
    for appointment in existing_appointments:
        # Получаем услугу для существующей записи, чтобы узнать её длительность
        existing_service = await get_service_by_id(db, appointment.service_id)
        if not existing_service:
            continue
        
        # Определяем занятые кварталы для этой записи
        start_quarter = appointment.quarter
        end_quarter = appointment.quarter + existing_service.duration_quarters - 1
        
        # Добавляем все кварталы от start до end включительно
        for q in range(start_quarter, end_quarter + 1):
            if 1 <= q <= 20:
                busy_quarters.add(q)
    
    # Определяем свободные кварталы
    # Квартал считается свободным, если с него можно начать запись длительностью service_duration
    # без выхода за границы и без наложения на занятые кварталы
    free_quarters = []
    
    for start_quarter in range(1, 21):
        # Проверяем, что запись не выходит за границы
        end_quarter = start_quarter + service_duration - 1
        if end_quarter > 20:
            continue
        
        # Проверяем, что все кварталы в этом интервале свободны
        is_free = True
        for q in range(start_quarter, end_quarter + 1):
            if q in busy_quarters:
                is_free = False
                break
        
        if is_free:
            free_quarters.append(start_quarter)
    
    return free_quarters

