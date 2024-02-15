from models.public import User
from repositories.user import UserRepository
from schemas.user import UserCreate


class UserServiceError(Exception):
    pass


class UserNotFoundError(UserServiceError):
    pass


class UserAlreadyExistsError(UserServiceError):
    pass


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    async def get_by_login(self, login: str) -> User:
        user = await self._user_repository.get_by_login(login)
        if user is None:
            raise UserNotFoundError(f"User with given login ({login}) not found")
        return user

    async def get_by_id(self, id: int) -> User:
        user = await self._user_repository.get(id)
        if user is None:
            raise UserNotFoundError(f"User with given id ({id}) not found")
        return user

    async def create(self, user_create_schema: UserCreate, password_hash: str) -> User:
        if await self._user_repository.exits_with_login(user_create_schema.login):
            raise UserAlreadyExistsError()
        user = User(
            **user_create_schema.model_dump(exclude={"password"}),
            password_hash=password_hash,
        )
        await self._user_repository.add(user)
        return user
    
    async def delete(self, user_id: int) -> None:
        await self._user_repository.update(user_id, {"deleted": True})
