from fastapi import Depends
from repositories.dependencies import get_alchemy_repository
from repositories.workspace import WorkspaceRepository
from services.workspace import (
    OperationNotPermittedError,
    WorkspaceNotFoundError,
    WorkspaceService,
)
from .user import get_logged_user, get_user_service
import models.public as public
from exceptions.workspace import workspace_not_found, operation_not_permitted


def get_workspace_service(
    workspace_repository: WorkspaceRepository = Depends(
        get_alchemy_repository(WorkspaceRepository)
    ),
) -> WorkspaceService:
    return WorkspaceService(workspace_repository)


async def get_workspace(
    workspace_id: int,
    user: public.User = Depends(get_logged_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> public.Workspace:
    try:
        return await workspace_service.get(workspace_id, user)
    except (WorkspaceNotFoundError, OperationNotPermittedError):
        raise workspace_not_found


async def get_logged_user_in_workspace(
    user: public.User = Depends(get_logged_user),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> public.User:
    if not await workspace_service.is_user_in_workspace(workspace, user):
        raise operation_not_permitted
    return user


async def get_workspace_admin(
    user: public.User = Depends(get_logged_user_in_workspace),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> public.User:
    if not workspace_service.is_user_admin(workspace, user):
        raise operation_not_permitted
    return user

