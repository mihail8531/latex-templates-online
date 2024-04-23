from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from repositories.dependencies import get_alchemy_repository
from repositories.user import UserRepository
from services.auth import AuthService, InvalidTokenError, TokenNotProvided
from services.user import UserService
from models.public import User
from exceptions.auth import credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


def get_user_service(
    user_repository: UserRepository = Depends(get_alchemy_repository(UserRepository)),
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


async def get_logged_user(
    token: str | None = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    try:
        user = await auth_service.get_authenticated_user_by_token(token)
    except (TokenNotProvided, InvalidTokenError):
        raise credentials_exception
    return user
