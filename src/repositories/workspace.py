from .repository import AlchemyIdRepository
from models.public import User, Workspace, UserWorkspace
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class WorkspaceRepository(AlchemyIdRepository[Workspace, int]):
    alchemy_model = Workspace

    async def get_all_by_participant_id(self, user_id: int) -> list[Workspace]:
        stmt = select(Workspace).join(
            UserWorkspace, onclause=(UserWorkspace.user_id == user_id)  # type: ignore[attr-defined]
        )
        return list((await self.session.execute(stmt)).scalars().all())
