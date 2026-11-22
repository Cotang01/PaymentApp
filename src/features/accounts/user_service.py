from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.features.accounts import user_repository as user_repo
from src.features.accounts.dto import UserCreateDTO
from src.features.accounts.models import User
from src.features.accounts.schemas import UserCreate, UserPatch, UserUpdate


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


async def get_user_list(
    db: AsyncSession, 
    offset: int, 
    limit: int
    ) -> Sequence[User]:
    return await user_repo.get_user_list(db, offset, limit)


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await user_repo.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundError(f"User with id {user_id} does not exists")
    return user


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    user_dto = UserCreateDTO(
        first_name=user.first_name,
        second_name=user.second_name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    new_user = await user_repo.create_user(db, user_dto)
    if new_user is None:
        raise UserAlreadyExistsError(
            f"User already exists with such email: {user.email}"
        )
    return new_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    res = await user_repo.delete_user(db, user_id)
    if not res:
        raise UserNotFoundError(f"User with id {user_id} does not exist")
    return res


async def update_user(
    db: AsyncSession, user_id: int, user_data: UserUpdate, current_user: User
    ) -> User:
    if not current_user.is_superuser and current_user.id != user_id:
        raise PermissionDeniedError("You can not change other users")
    changed_data = user_data.model_dump()
    changed_data["hashed_password"] = get_password_hash(changed_data.pop("password"))
    user = await user_repo.update_user(db, user_id, changed_data)
    if not user:
        raise UserNotFoundError(f"User with id {user_id} does not exist")
    return user


async def patch_user(
    db: AsyncSession, user_id: int, user_data: UserPatch, current_user: User
    ) -> User:
    if not current_user.is_superuser and current_user.id != user_id:
        raise PermissionDeniedError("You can not change other users")
    changed_data = user_data.model_dump(exclude_unset=True)
    if "password" in changed_data:
        changed_data["hashed_password"] = get_password_hash(changed_data.pop("password"))
    user = await user_repo.update_user(db, user_id, changed_data)
    if not user:
        raise UserNotFoundError(f"User with id {user_id} does not exist")
    return user
