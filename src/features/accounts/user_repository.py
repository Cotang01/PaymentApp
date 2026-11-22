from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.accounts.dto import UserCreateDTO
from src.features.accounts.models import User


class DuplicateEmailError(Exception):
    pass


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = (
        select(User)
        .where(User.id == user_id)
        )
    return (await db.execute(stmt)).scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = (
        select(User)
        .where(User.email == email)
        )
    return (await db.execute(stmt)).scalar_one_or_none()


async def get_user_list(
    db: AsyncSession, 
    offset: int, 
    limit: int
    ) -> Sequence[User]:
    stmt = (
        select(User)
        .offset(offset)
        .limit(limit)
        )
    return (await db.scalars(stmt)).all()


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    stmt = (
        delete(User)
        .where(User.id == user_id)
        .returning(User.id)
        )
    res = await db.execute(stmt)
    return res.scalar_one_or_none() is not None


async def create_user(db: AsyncSession, user_dto: UserCreateDTO) -> User | None:
    stmt = (
        insert(User)
        .values(user_dto.model_dump())
        .returning(User)
        )
    try:
        user = (await db.execute(stmt)).scalar_one_or_none()
        return user
    except IntegrityError as e:
        await db.rollback()
        raise DuplicateEmailError(
            f"User with email {user_dto.email} already exists"
            ) from e


async def update_user(db: AsyncSession, 
                      user_id: int, 
                      user_data: dict[str, Any]) -> User | None:
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(user_data)
        .returning(User))
    try:
        user = (await db.execute(stmt)).scalar_one_or_none()
        return user
    except IntegrityError as e:
        await db.rollback()
        raise DuplicateEmailError(
            f"User with email {user_data['email']} already exists"
            ) from e
