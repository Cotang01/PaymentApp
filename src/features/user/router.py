from fastapi import APIRouter

from src.core.dependencies import DbSession
from src.features.user.schemas import UserCreate, UserResponse
from src.features.user.service import get_user_list as service_get_user_list

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse)
async def create_user(db: DbSession, user: UserCreate):
    pass


@router.delete("/{user_id}")
async def delete_user(db: DbSession, user_id: int):
    pass


@router.get("", response_model=list[UserResponse])
async def get_users(db: DbSession):
    return await service_get_user_list(db)
