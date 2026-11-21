from fastapi import APIRouter, status

from src.core.dependencies import DbSession
from src.features.accounts import user_service
from src.features.accounts.dependencies import CurrentUser
from src.features.accounts.schemas import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


@router.post("", response_model=UserResponse)
async def create_user(db: DbSession, user: UserCreate):
    return await user_service.create_user(db, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: DbSession, user_id: int):
    return await user_service.delete_user(db, user_id)


@router.get("", response_model=list[UserResponse])
async def get_users(db: DbSession):  # TODO: pagination 
    return await user_service.get_user_list(db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(db: DbSession, user_id: int):
    return await user_service.get_user_by_id(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(db: DbSession, user_id: int, new_data: UserPatch):
    return await user_service.patch_user(db, user_id, new_data)
    

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(db: DbSession, user_id: int, new_data: UserUpdate):
    return await user_service.update_user(db, user_id, new_data)
