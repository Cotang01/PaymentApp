from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.features.accounts.auth_service import (
    InvalidCredentialsError,
    SessionNotFoundError,
)
from src.features.accounts.user_repository import DuplicateEmailError
from src.features.accounts.user_service import (
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
