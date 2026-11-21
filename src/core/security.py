import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from src.app.config import settings

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": str(user_id),
        "type": "access",
        "exp": datetime.now(UTC) 
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload=payload, 
                      key=settings.SECRET_KEY, 
                      algorithm=settings.ALGORITHM)


def generate_raw_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def get_refresh_token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
