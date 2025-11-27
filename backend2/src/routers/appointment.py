from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth import get_current_user
from src.models.user import User
from src.models.service import Service
from src.models.appointment import Appointment
from src.schemas.appointment import AppointmentCreate, AppointmentListResponse, AppointmentDetailResponse
from src.crud.appointment import (
    get_all_appointments,
    get_appointment_by_id,
    create_appointment,
    delete_appointment,
    validate_appointment,
    get_appointments_by_client,
    get_appointments_by_master
)
from src.crud.user import get_user_by_id
from src.crud.service import get_service_by_id

router = APIRouter(prefix="/appointments")


def build_appointment_response(appointment: Appointment, client: User, service: Service, master: User) -> AppointmentListResponse:
    """Вспомогательная функция для построения ответа из записи"""
    return AppointmentListResponse(
        id=appointment.id,
        date=appointment.date,
        quarter=appointment.quarter,
        status=appointment.status,
        is_paid=appointment.is_paid,
        master_full_name=master.full_name,
        service_title=service.title,
        service_price=service.price,
        client_full_name=client.full_name
    )


async def get_appointments_with_details(
    db: AsyncSession,
    appointments: list[Appointment]
) -> list[AppointmentListResponse]:
    """Получает список записей с полной информацией"""
    result = []
    for appointment in appointments:
        # Получаем информацию о клиенте
        client = await get_user_by_id(db, appointment.client_id)
        # Получаем информацию об услуге
        service = await get_service_by_id(db, appointment.service_id)
        if service:
            # Получаем информацию о мастере
            master = await get_user_by_id(db, service.master_id)
            if client and master:
                result.append(build_appointment_response(appointment, client, service, master))
    return result


@router.get("", response_model=list[AppointmentListResponse])
async def get_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение списка всех записей"""
    appointments = await get_all_appointments(db)
    return await get_appointments_with_details(db, appointments)


@router.get("/client", response_model=list[AppointmentListResponse])
async def get_client_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение записей текущего клиента"""
    appointments = await get_appointments_by_client(db, current_user.id)
    return await get_appointments_with_details(db, appointments)


@router.get("/master", response_model=list[AppointmentListResponse])
async def get_master_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение записей текущего мастера"""
    appointments = await get_appointments_by_master(db, current_user.id)
    return await get_appointments_with_details(db, appointments)


@router.get("/{appointment_id}", response_model=AppointmentDetailResponse)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение записи по ID"""
    appointment = await get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Получаем информацию о клиенте
    client = await get_user_by_id(db, appointment.client_id)
    # Получаем информацию об услуге
    service = await get_service_by_id(db, appointment.service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Получаем информацию о мастере
    master = await get_user_by_id(db, service.master_id)
    if not master or not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related entity not found"
        )
    
    return AppointmentDetailResponse(
        id=appointment.id,
        date=appointment.date,
        quarter=appointment.quarter,
        status=appointment.status,
        is_paid=appointment.is_paid,
        master_full_name=master.full_name,
        service_title=service.title,
        service_price=service.price,
        client_full_name=client.full_name
    )


@router.post("", response_model=AppointmentDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment_endpoint(
    appointment_create: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создание новой записи с валидацией"""
    # Проверяем, существует ли клиент
    client = await get_user_by_id(db, appointment_create.client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Проверяем, существует ли услуга
    service = await get_service_by_id(db, appointment_create.service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Валидация записи: проверка границ кварталов и наложения с другими записями
    is_valid, error_message = await validate_appointment(
        db=db,
        service_id=appointment_create.service_id,
        appointment_date=appointment_create.date,
        quarter=appointment_create.quarter,
        duration_quarters=service.duration_quarters
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    appointment = await create_appointment(db, appointment_create)
    
    # Получаем информацию о мастере для ответа
    master = await get_user_by_id(db, service.master_id)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    return AppointmentDetailResponse(
        id=appointment.id,
        date=appointment.date,
        quarter=appointment.quarter,
        status=appointment.status,
        is_paid=appointment.is_paid,
        master_full_name=master.full_name,
        service_title=service.title,
        service_price=service.price,
        client_full_name=client.full_name
    )


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment_endpoint(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление записи"""
    deleted = await delete_appointment(db, appointment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

