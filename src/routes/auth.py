from fastapi import APIRouter, Depends
from exceptions.utils import with_errors
from exceptions.auth import credentials_exception
from schemas.auth import Token
from services.auth import AuthService, InvalidPasswordError
from dependencies.user import get_auth_service
from .forms import PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/token", responses=with_errors(credentials_exception))
async def get_token(
    form_data: PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """
    Получить JWT токен для авторизации.
    """
    try:
        user = await auth_service.get_authenticated_user(
            form_data.username, form_data.password
        )
    except InvalidPasswordError:
        raise credentials_exception
    return await auth_service.get_token(user.id)
