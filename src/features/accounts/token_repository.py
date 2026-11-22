from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.config import settings
from src.features.accounts.models import RefreshToken


async def get_refresh_token_by_hash(
    db: AsyncSession, refresh_hash: str
    ) -> RefreshToken | None:
    stmt = (
        select(RefreshToken)
        .where(RefreshToken.token_hash == refresh_hash)
        )
    return (await db.execute(stmt)).scalar_one_or_none()


async def rotate_refresh_token(
    db: AsyncSession, current_refresh_hash: str, new_refresh_hash: str
    ) -> int | None:
    now = datetime.now(UTC)
    stmt = (
        update(RefreshToken)
        .where(
            RefreshToken.token_hash == current_refresh_hash,
            RefreshToken.exp > now,
            RefreshToken.abs_exp > now,
            RefreshToken.revoked_at.is_(None))
        .values(token_hash=new_refresh_hash,
                exp=func.least(
                    now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), 
                    RefreshToken.abs_exp))
        .returning(RefreshToken.user_id)
        )
    return (await db.execute(stmt)).scalar_one_or_none()


async def delete_refresh_token(db: AsyncSession, token_hash: str) -> bool:
    stmt = (
        delete(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .returning(RefreshToken)
        )
    return (await db.execute(stmt)).scalar_one_or_none() is not None


async def revoke_refresh_token(db: AsyncSession, token_hash: str) -> bool:
    stmt = (
        update(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .values(revoked_at=datetime.now(UTC))
        .returning(RefreshToken)
    )
    return (await db.execute(stmt)).scalar_one_or_none() is not None


async def create_refresh_token(db: AsyncSession, 
                               user_id: int, 
                               token_hash: str) -> RefreshToken:
    now = datetime.now(UTC)
    stmt = (
        insert(RefreshToken)
        .values(user_id=user_id, 
                token_hash=token_hash, 
                exp=now
                    + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                abs_exp=now
                    + timedelta(days=settings.REFRESH_TOKEN_ABS_EXPIRE_DAYS)
                )
        .returning(RefreshToken)
        )
    return (await db.execute(stmt)).scalar_one()


async def get_refresh_tokens(db: AsyncSession, offset: int, limit: int):
     stmt = (
        select(RefreshToken)
        .offset(offset)
        .limit(limit)
        )
     return (await db.execute(stmt)).scalars().all()