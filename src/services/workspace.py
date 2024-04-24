from models import public
from repositories.workspace import WorkspaceRepository
from schemas.workspace import WorkspaceCreate


class WorkspaceService:
    def __init__(self, workspace_repository: WorkspaceRepository) -> None:
        self._workspace_repository = workspace_repository

    async def create(
        self, workspace_create: WorkspaceCreate, creator_id: int
    ) -> public.Workspace:
        workspace = public.Workspace(
            creator_id=creator_id,
            admin_id=creator_id,
            name=workspace_create.name,
            description=workspace_create.description,
        )
        await self._workspace_repository.add(workspace)
        return workspace

    async def get_all_by_participant(self, user_id: int) -> list[public.Workspace]:
        return await self._workspace_repository.get_all_by_participant_id(user_id)
