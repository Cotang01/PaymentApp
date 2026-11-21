from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Response, status

from src.app.config import settings
from src.core.dependencies import AccessToken, DbSession
from src.features.accounts.models import User
from src.features.accounts.user_service import get_user_by_id


async def get_current_user(
    db: DbSession, 
    access_token: AccessToken
    ) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, 
                             settings.SECRET_KEY, 
                             algorithms=[settings.ALGORITHM])
        if payload["type"] != "access":
            raise credentials_exception
        user = await get_user_by_id(db, int(payload["user_id"]))
        if user is None:
            raise credentials_exception
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_exception
    
    
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_admin_user(user: CurrentUser) -> User:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user


AdminUser = Annotated[User, Depends(get_admin_user)]


def set_refresh_in_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.DEBUG,  # True requires HTTPS
        samesite="lax",
        path="/auth"
    )
