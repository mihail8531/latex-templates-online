from fastapi import APIRouter, Depends
from dependencies.user import get_logged_user
from dependencies.workspace import get_workspace_service
from models import public
from schemas.workspace import Workspace, WorkspaceBase, WorkspaceCreate, WorkspaceHeader
from services.workspace import WorkspaceService
from .utils import validate_ta

workspace_router = APIRouter(prefix="/workspace")


@workspace_router.post("/create")
async def create_workspace(
    workspace_create: WorkspaceCreate,
    user: public.User = Depends(get_logged_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> Workspace:
    workspace = await workspace_service.create(workspace_create, user.id)
    return Workspace.model_validate(workspace, from_attributes=True)


@workspace_router.get("/list")
async def get_user_workspaces(
    user: public.User = Depends(get_logged_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> list[WorkspaceHeader]:
    workspaces = await workspace_service.get_all_by_participant(user.id)
    return validate_ta(list[WorkspaceHeader], workspaces)

# @workspace_router.get("/{id}")
# async def get_workspace(
#     user: public.User = Depends(get_logged_user)
# )

