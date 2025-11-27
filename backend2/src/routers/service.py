from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth import get_current_user
from src.models.user import User
from src.models.service import Service
from src.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceListResponse, FreeQuartersResponse
from src.crud.appointment import get_free_quarters
from src.crud.service import (
    get_all_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service,
    get_services_by_master_id
)
from src.crud.user import get_user_by_id

router = APIRouter(prefix="/services")


@router.get("", response_model=list[ServiceListResponse])
async def get_services(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение списка всех услуг с информацией о мастере"""
    services = await get_all_services(db)
    
    result = []
    for service in services:
        # Получаем информацию о мастере
        master = await get_user_by_id(db, service.master_id)
        if master:
            result.append(ServiceListResponse(
                id=service.id,
                title=service.title,
                price=service.price,
                duration_quarters=service.duration_quarters,
                master_id=service.master_id,
                master_full_name=master.full_name,
                master_role=master.role,
                master_phone_number=master.phone_number
            ))
    
    return result


@router.get("/masters/{master_id}", response_model=list[ServiceListResponse])
async def get_master_services(
    master_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение услуг мастера по его ID"""
    # Проверяем, существует ли мастер
    master = await get_user_by_id(db, master_id)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    services = await get_services_by_master_id(db, master_id)
    
    result = []
    for service in services:
        result.append(ServiceListResponse(
            id=service.id,
            title=service.title,
            price=service.price,
            duration_quarters=service.duration_quarters,
            master_id=service.master_id,
            master_full_name=master.full_name,
            master_role=master.role,
            master_phone_number=master.phone_number
        ))
    
    return result


@router.get("/{service_id}/free_quarters", response_model=FreeQuartersResponse)
async def get_free_quarters_endpoint(
    service_id: int,
    date: date = Query(..., description="Date for checking free quarters"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение свободных кварталов для услуги на указанную дату"""
    # Проверяем, существует ли услуга
    service = await get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    free_quarters = await get_free_quarters(db, service_id, date)
    return FreeQuartersResponse(free_quarters=free_quarters)


@router.get("/{service_id}", response_model=ServiceListResponse)
async def get_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение услуги по ID"""
    service = await get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    master = await get_user_by_id(db, service.master_id)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    return ServiceListResponse(
        id=service.id,
        title=service.title,
        price=service.price,
        duration_quarters=service.duration_quarters,
        master_id=service.master_id,
        master_full_name=master.full_name,
        master_role=master.role,
        master_phone_number=master.phone_number
    )


@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service_endpoint(
    service_create: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создание новой услуги"""
    # Проверяем, существует ли мастер
    master = await get_user_by_id(db, service_create.master_id)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found"
        )
    
    service = await create_service(db, service_create)
    return ServiceResponse.model_validate(service)


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service_endpoint(
    service_id: int,
    service_update: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление услуги"""
    # Если обновляется master_id, проверяем существование мастера
    if service_update.master_id is not None:
        master = await get_user_by_id(db, service_update.master_id)
        if not master:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Master not found"
            )
    
    service = await update_service(db, service_id, service_update)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return ServiceResponse.model_validate(service)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_endpoint(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление услуги"""
    deleted = await delete_service(db, service_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )

