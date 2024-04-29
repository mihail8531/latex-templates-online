from .repository import AlchemyIdRepository
from models.public import User, Workspace, user_workspace
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class WorkspaceRepository(AlchemyIdRepository[Workspace, int]):
    alchemy_model = Workspace

    async def get_all_by_participant_id(self, user_id: int) -> list[Workspace]:
        stmt = (
            select(Workspace)
            .join(
                user_workspace, onclause=(Workspace.id == user_workspace.c.workspace_id)
            )
            .where(user_workspace.c.user_id == user_id)
        )
        return list((await self.session.execute(stmt)).scalars().all())

    async def get_users(self, workspace: Workspace) -> list[User]:
        return await workspace.awaitable_attrs.users

    async def get_full(self, workspace: Workspace) -> Workspace:
        await workspace.awaitable_attrs.admin
        await workspace.awaitable_attrs.creator
        await workspace.awaitable_attrs.users
        await workspace.awaitable_attrs.templates
        return workspace

    async def add_user(self, workspace: Workspace, user: User) -> None:
        (await workspace.awaitable_attrs.users).append(user)
        await self.session.flush()
        await self.session.refresh(workspace)

    async def delete_user(self, workspace: Workspace, user: User) -> None:
        (await workspace.awaitable_attrs.users).remove(user)
        await self.session.flush()
        await self.session.refresh(workspace)
