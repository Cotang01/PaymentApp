from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    create_access_token,
    generate_raw_refresh_token,
    get_refresh_token_hash,
    verify_password,
)
from src.features.accounts import token_repository as token_repo
from src.features.accounts import user_repository as user_repo
from src.features.accounts import user_service
from src.features.accounts.models import RefreshToken
from src.features.accounts.schemas import UserCreate


class SessionNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


async def invalidate_refresh_token(
    db: AsyncSession, current_refresh: str | None
    ) -> None:
    if current_refresh is None:
        raise SessionNotFoundError("No refresh token provided")
    revoked = await token_repo.revoke_refresh_token(
        db, get_refresh_token_hash(current_refresh)
        )
    if not revoked:
        raise SessionNotFoundError("Failed to revoke refresh token")


async def rotate_refresh_token(db: AsyncSession, 
                                current_refresh: str | None) -> dict[str, str]:
    if current_refresh is None:
        raise SessionNotFoundError("No refresh token provided")
    new_refresh = generate_raw_refresh_token()
    user_id = await token_repo.rotate_refresh_token(
        db, 
        get_refresh_token_hash(current_refresh), 
        get_refresh_token_hash(new_refresh)
        )
    if user_id is None:
        raise SessionNotFoundError("Did not find valid refresh token")
    new_access = create_access_token(user_id)
    return {"access_token": new_access, "refresh_token": new_refresh}


async def get_refresh_token_by_hash(
    db: AsyncSession, raw_refresh: str
    ) -> RefreshToken:
    refresh_token_obj = await token_repo.get_refresh_token_by_hash(
        db, get_refresh_token_hash(raw_refresh)
        )
    if refresh_token_obj is None:
        raise SessionNotFoundError("Refresh token not found")
    return refresh_token_obj


async def register(db: AsyncSession, data: UserCreate) -> dict[str, str]:
    await user_service.create_user(db, data)
    tokens = await login(db, data.email, data.password)
    return tokens


async def login(db: AsyncSession, 
                email: str, 
                password: str) -> dict[str, str]:
    user = await user_repo.get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid email or password")
    access = create_access_token(user.id)
    raw_refresh = generate_raw_refresh_token()
    refresh_hash = get_refresh_token_hash(raw_refresh)
    await token_repo.create_refresh_token(db, user.id, refresh_hash)
    return {"access_token": access, "refresh_token": raw_refresh}


async def get_refresh_tokens(db: AsyncSession, offset: int, limit: int):
    return await token_repo.get_refresh_tokens(db, offset, limit)