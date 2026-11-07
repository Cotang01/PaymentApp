from pwdlib import PasswordHash

from src.app.config import settings

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(hashed_password, plain_password)


# TODO implement token creation and verification functions
