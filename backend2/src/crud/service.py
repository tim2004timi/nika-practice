from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from src.models.service import Service
from src.schemas.service import ServiceCreate, ServiceUpdate


async def get_all_services(db: AsyncSession) -> list[Service]:
    """Получает все услуги с информацией о мастере"""
    result = await db.execute(
        select(Service)
    )
    return list(result.scalars().all())


async def get_services_by_master_id(db: AsyncSession, master_id: int) -> list[Service]:
    """Получает все услуги мастера по его ID"""
    result = await db.execute(
        select(Service).where(Service.master_id == master_id)
    )
    return list(result.scalars().all())


async def get_service_by_id(db: AsyncSession, service_id: int) -> Optional[Service]:
    """Получает услугу по ID"""
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    return result.scalar_one_or_none()


async def create_service(db: AsyncSession, service_create: ServiceCreate) -> Service:
    """Создает новую услугу"""
    db_service = Service(
        title=service_create.title,
        duration_quarters=service_create.duration_quarters,
        price=service_create.price,
        master_id=service_create.master_id
    )
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service


async def update_service(
    db: AsyncSession, 
    service_id: int, 
    service_update: ServiceUpdate
) -> Optional[Service]:
    """Обновляет услугу (частичное обновление)"""
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    db_service = result.scalar_one_or_none()
    
    if not db_service:
        return None
    
    update_data = service_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_service, field, value)
    
    await db.commit()
    await db.refresh(db_service)
    return db_service


async def delete_service(db: AsyncSession, service_id: int) -> bool:
    """Удаляет услугу"""
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    db_service = result.scalar_one_or_none()
    
    if not db_service:
        return False
    
    await db.delete(db_service)
    await db.commit()
    return True

