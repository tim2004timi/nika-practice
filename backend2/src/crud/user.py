from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.utils import get_password_hash


async def get_user_by_login(db: AsyncSession, login: str) -> Optional[User]:
    """Получает пользователя по логину"""
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Получает пользователя по ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    """Создает нового пользователя с хешированием пароля"""
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        login=user_create.login,
        password_hash=hashed_password,
        full_name=user_create.full_name,
        phone_number=user_create.phone_number,
        role=user_create.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_all_masters(db: AsyncSession) -> list[dict]:
    """Получает всех мастеров (пользователей с ролью != CLIENT) с подсчетом количества услуг"""
    from src.models.service import Service
    
    # Подзапрос для подсчета услуг
    services_count_subquery = (
        select(func.count(Service.id))
        .where(Service.master_id == User.id)
        .scalar_subquery()
    )
    
    # Основной запрос
    result = await db.execute(
        select(
            User.id,
            User.full_name,
            User.role,
            User.phone_number,
            services_count_subquery.label("services_count")
        ).where(User.role != "CLIENT")
    )
    
    rows = result.all()
    return [
        {
            "id": row.id,
            "full_name": row.full_name,
            "role": row.role,
            "phone_number": row.phone_number,
            "services_count": row.services_count or 0
        }
        for row in rows
    ]


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_update: UserUpdate
) -> Optional[User]:
    """Обновляет пользователя (частичное обновление)"""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

