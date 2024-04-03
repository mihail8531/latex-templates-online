from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from repositories.dependencies import get_alchemy_repository
from repositories.user import UserRepository
from services.auth import AuthService
from services.user import UserService


class OAuth2CookiePasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            return None
        return param


oauth2_scheme = OAuth2CookiePasswordBearer(tokenUrl="auth/token", auto_error=False)


def get_user_service(
    user_repository: UserRepository = Depends(get_alchemy_repository(UserRepository)),
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)
