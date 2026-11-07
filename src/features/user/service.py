from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.features.user.models import User
from src.features.user.repository import get_user_by_id as repo_get_user_by_id
from src.features.user.repository import get_user_list as repo_get_user_list


class UserNotFoundError(Exception):
    pass


async def get_user_list(db: AsyncSession) -> Sequence[User]:
    return await repo_get_user_list(db)


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await repo_get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundError(f"User with id {user_id} does not exists")
    return user
