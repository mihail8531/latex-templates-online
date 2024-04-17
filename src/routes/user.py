from typing import Annotated
from fastapi import APIRouter, Depends, Response, Form

from dependencies.user import get_user_service
from services.user import UserService
from schemas.user import UserCreate

user_router = APIRouter(prefix="/user")


# @user_router.get("/me")
# async def get_current_user(user: User = Depends(get_user)) -> UserSchema:
#     return UserSchema.model_validate(user, from_attributes=True)


# @user_router.delete("/me")
# async def delete_current_user(
#     user: User = Depends(get_user),
#     user_service: UserService = Depends(get_user_service),
# ) -> None:
#     await user_service.delete(user.id)


# @user_router.post("/create")
# async def create_user(
#     user_create_schema: UserSchema,
#     user_service: UserService = Depends(get_user_service),
#     auth_service: AuthService = Depends(get_auth_service),
# ) -> UserSchema:
#     password_hash = auth_service.get_password_hash(user_create_schema.password)
#     try:
#         user = await user_service.create(user_create_schema, password_hash)
#     except UserAlreadyExistsError:
#         raise user_already_exists
#     return UserSchema.model_validate(user, from_attributes=True)


@user_router.post("/create")
async def create_user(
    login: str = Form(),
    password: str = Form(),
    display_name: str | None = Form(),
    email: str | None = Form(),
    user_service: UserService = Depends(get_user_service)
) -> Response:
    try:
        create_schema = UserCreate(login=login, display_name=display_name, password=password)
    user_service.create()
    
