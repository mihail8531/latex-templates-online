from .repository import AlchemyIdRepository
from models.public import User
from sqlalchemy import select


class UserRepository(AlchemyIdRepository[User, int]):
    alchemy_model = User

    async def get_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def exits_with_login(self, login: str) -> bool:
        stmt = select(User.id).where(User.login == login)
        return (await self.session.execute(stmt)).scalar_one_or_none() is not None
