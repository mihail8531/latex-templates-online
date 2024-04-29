from .repository import AlchemyIdRepository
from models.public import User, Workspace
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class UserRepository(AlchemyIdRepository[User, int]):
    alchemy_model = User

    async def get_by_login(self, login: str) -> User | None:
        stmt = (
            select(User).where(User.login == login).options(joinedload(User.workspaces))
        )
        return (await self.session.execute(stmt)).unique().scalar_one_or_none()

    async def exits_with_login(self, login: str) -> bool:
        stmt = select(User.id).where(User.login == login)
        return (await self.session.execute(stmt)).scalar_one_or_none() is not None

    async def get_workspaces(self, user: User) -> list[Workspace]:
        return await user.awaitable_attrs.workspaces

    async def add_workspace(self, user: User, workspace: Workspace) -> None:
        (await user.awaitable_attrs.workspaces).append(workspace)
