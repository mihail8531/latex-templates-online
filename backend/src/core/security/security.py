from datetime import datetime, timedelta
from typing import Union

from jose import jwt
from passlib.context import CryptContext

from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
    access_token_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    secret_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
):
    if expires_delta is None:
        expires_delta = timedelta(minutes=access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, **data}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
