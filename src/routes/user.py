from typing import Annotated
from fastapi import APIRouter, Depends

from dependencies.user import get_auth_service, get_logged_user, get_user_service
from exceptions.user import user_already_exists, user_not_found
from models import public
from services.auth import AuthService
from services.user import UserAlreadyExistsError, UserNotFoundError, UserService
from schemas.user import UserCreate, UserHeader

user_router = APIRouter(prefix="/user")


@user_router.get("/me")
async def get_current_user(user: public.User = Depends(get_logged_user)) -> UserHeader:
    return UserHeader.model_validate(user, from_attributes=True)


@user_router.delete("/me")
async def delete_current_user(
    user: public.User = Depends(get_logged_user),
    user_service: UserService = Depends(get_user_service),
) -> None:
    await user_service.delete(user.id)


@user_router.post("/create")
async def create_user(
    user_create_schema: UserCreate,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserHeader:
    password_hash = auth_service.get_password_hash(
        user_create_schema.password.get_secret_value()
    )
    try:
        user = await user_service.create(user_create_schema, password_hash)
    except UserAlreadyExistsError:
        raise user_already_exists
    return UserHeader.model_validate(user, from_attributes=True)


@user_router.get("/")
async def get_user(
    login: str,
    current_user: public.User = Depends(get_logged_user),
    user_service: UserService = Depends(get_user_service),
) -> UserHeader:
    try:
        user = await user_service.get_by_login(login)
    except UserNotFoundError:
        raise user_not_found
    return UserHeader.model_validate(user, from_attributes=True)
