from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.features.accounts.auth_service import (
    InvalidCredentialsError,
    SessionNotFoundError,
)
from src.features.accounts.dependencies import InvalidAccessToken
from src.features.accounts.user_repository import DuplicateEmailError
from src.features.accounts.user_service import (
    PermissionDeniedError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request, exc: UserAlreadyExistsError
        ):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
                            content={"detail": str(exc)})

    @app.exception_handler(DuplicateEmailError)
    async def duplicate_email_handler(
        request: Request, exc: DuplicateEmailError
        ):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
                            content={"detail": str(exc)})

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request, exc: UserNotFoundError
        ):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"detail": str(exc)})
    
    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_handler(
        request: Request, exc: SessionNotFoundError
        ):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, 
                            content={"detail": str(exc)})
    
    @app.exception_handler(InvalidCredentialsError)
    async def ivalid_credentials_handler(
        request: Request, exc: InvalidCredentialsError
        ):
         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, 
                            content={"detail": str(exc)})

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied_handler(
        request: Request, exc: PermissionDeniedError
        ):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, 
                            content={"detail": str(exc)})
    
    @app.exception_handler(InvalidAccessToken)
    async def invalid_access_token_handler(
        request: Request, exc: InvalidAccessToken
        ):
         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, 
                            content={"detail": str(exc)},
                            headers={"WWW-Authenticate": "Bearer"})