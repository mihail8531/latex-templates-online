from fastapi import Depends
from repositories.dependencies import get_alchemy_repository
from repositories.workspace import WorkspaceRepository
from services.workspace import WorkspaceService


def get_workspace_service(
    workspace_repository: WorkspaceRepository = Depends(
        get_alchemy_repository(WorkspaceRepository)
    ),
) -> WorkspaceService:
    return WorkspaceService(workspace_repository)
