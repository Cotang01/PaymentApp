from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]

DbSession = Annotated[AsyncSession, Depends(get_db)]

AccessToken = Annotated[str, Depends(oauth2_scheme)]
