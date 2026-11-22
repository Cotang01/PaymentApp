from fastapi import APIRouter, Request, Response

from src.core.dependencies import AuthForm, DbSession
from src.features.accounts import auth_service
from src.features.accounts.dependencies import (
    AdminUser,
    CurrentUser,
    set_refresh_in_cookie,
)
from src.features.accounts.schemas import AccessTokenResponse, UserCreate

router = APIRouter(prefix="/auth")


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(db: DbSession, request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    tokens = await auth_service.rotate_refresh_token(db, refresh_token)
    set_refresh_in_cookie(response, tokens["refresh_token"])
    return tokens


@router.post("/logout")
async def logout(
    db: DbSession, 
    request: Request, 
    response: Response, 
    current_user: CurrentUser
    ):
    refresh_token = request.cookies.get("refresh_token")
    await auth_service.invalidate_refresh_token(db, refresh_token)
    response.delete_cookie("refresh_token", path="/auth")
    

@router.post("/login", response_model=AccessTokenResponse)
async def login(db: DbSession, response: Response, form_data: AuthForm):
    tokens = await auth_service.login(db, form_data.username, form_data.password) 
                                   # username contains email
    set_refresh_in_cookie(response, tokens.pop("refresh_token"))
    return tokens


@router.post("/register", response_model=AccessTokenResponse)
async def register(db: DbSession, response: Response, data: UserCreate):
    tokens = await auth_service.register(db, data)
    set_refresh_in_cookie(response, tokens.pop("refresh_token"))
    return tokens


@router.get("/tokens")
async def get_refresh_tokens(db: DbSession, admin_user: AdminUser):
    return await auth_service.get_refresh_tokens(db)