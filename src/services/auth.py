import time

from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas.auth import Token

import settings
from models.public import User
from services.user import UserService


class AuthServiceError(Exception):
    pass


class InvalidPasswordError(AuthServiceError):
    pass


class InvalidTokenError(AuthServiceError):
    pass

class TokenNotProvided(AuthServiceError):
    pass


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        user_service: UserService,
        settings: settings.AuthSettings = settings.settings,
    ) -> None:
        self._user_service = user_service
        self._jwt_algorithm = settings.AUTH_HASH_ALGORITHM
        self._jwt_secret_key = settings.AUTH_SECRET_KEY
        self._jwt_duration = settings.AUTH_TOKEN_DURATION_SEC

    @property
    def jwt_duration(self) -> int:
        return self._jwt_duration

    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        return self.pwd_context.verify(plain_password, password_hash)

    def get_password_hash(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)

    async def get_authenticated_user(self, login: str, password: str) -> User:
        user = await self._user_service.get_by_login(login)
        if not self.verify_password(password, user.password_hash):
            raise InvalidPasswordError()
        return user

    async def get_authenticated_user_by_token(self, token: str | None) -> User:
        if token is None:
            raise TokenNotProvided()
        try:
            token_payload = jwt.decode(
                token, self._jwt_secret_key, algorithms=[self._jwt_algorithm]
            )
        except JWTError:
            raise InvalidTokenError(token)
        exp = token_payload.get("exp", None)
        if exp is None or exp < time.time():
            raise InvalidTokenError()
        id = token_payload.get("id", None)
        if id is None:
            raise InvalidTokenError()
        user = await self._user_service.get_by_id(id)
        return user

    def _get_access_token(self, user_id: int) -> str:
        return jwt.encode(
            {"id": user_id, "exp": time.time() + self._jwt_duration},
            self._jwt_secret_key,
            algorithm=self._jwt_algorithm,
        )

    async def get_token(self, user_id: int) -> Token:
        access_token = self._get_access_token(user_id)
        return Token(
            token_type="Bearer",
            access_token=access_token,
            expires_in=self._jwt_duration,
        )
