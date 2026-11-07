from collections.abc import Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.user.models import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return (await db.execute(stmt)).scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return (await db.execute(stmt)).scalar_one_or_none()


async def get_user_list(db: AsyncSession) -> Sequence[User]:  # TODO add chunking
    stmt = select(User)
    return (await db.scalars(stmt)).all()


async def delete_user(db: AsyncSession, user_id: int) -> bool:  # TODO add what fields to fetch
    stmt = delete(User).where(User.id == user_id).returning(User.id)
    res = await db.execute(stmt)
    await db.commit()  # for extra logic move .commit() to service layer
    return res.scalar_one_or_none() is not None


async def create_user(db: AsyncSession, user_data: dict[str, str]) -> User | None:
    stmt = insert(User).values(user_data).returning(User)
    try:
        user = (await db.execute(stmt)).scalar_one_or_none()
        await db.commit()  # for extra logic move .commit() to service layer
        return user
    except IntegrityError:
        await db.rollback()
        return None


async def update_user(db: AsyncSession, 
                      user_id: int, 
                      user_data: dict[str, str]) -> User | None:
    stmt = update(User).where(User.id == user_id).values(user_data).returning(User)
    try:
        user = (await db.execute(stmt)).scalar_one_or_none()
        await db.commit()  # for extra logic move .commit() to service layer
        return user
    except IntegrityError:
        await db.rollback()
        return None


