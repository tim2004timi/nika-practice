from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.auth import get_current_user
from src.models.user import User
from src.schemas.user import UserResponse, MasterResponse
from src.crud.user import get_all_masters

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Получение информации о текущем пользователе"""
    return UserResponse.model_validate(current_user)


@router.get("/masters", response_model=list[MasterResponse])
async def get_masters(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получение списка всех мастеров с количеством услуг"""
    masters = await get_all_masters(db)
    return [MasterResponse(**master) for master in masters]

