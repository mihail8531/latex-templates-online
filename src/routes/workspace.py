from fastapi import APIRouter, Depends
from dependencies.template import (
    get_template,
    get_template_author_or_admin,
    get_template_service,
)
from dependencies.user import get_logged_user, get_user, get_user_service
from dependencies.workspace import (
    get_logged_user_in_workspace,
    get_workspace as get_workspace,
    get_workspace_admin,
    get_workspace_service,
)
from models import public
from schemas.template import TemplateCreate, TemplateHeader, Template
from schemas.workspace import Workspace, WorkspaceBase, WorkspaceCreate, WorkspaceHeader
from services.template import TemplateService
from services.user import UserNotFoundError, UserService
from services.workspace import (
    OperationNotPermittedError,
    UserAlreadyInWorkspaceError,
    UserNotInWorkspaceError,
    WorkspaceService,
)
from .utils import validate_ta
from exceptions.workspace import (
    operation_not_permitted,
    user_not_in_workspace,
    user_already_in_workspace,
)

workspace_router = APIRouter(prefix="/workspace")


@workspace_router.post("/create")
async def create_workspace(
    workspace_create: WorkspaceCreate,
    user: public.User = Depends(get_logged_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> WorkspaceHeader:
    workspace = await workspace_service.create(workspace_create, user)
    await add_user(user, user, workspace, workspace_service)
    return WorkspaceHeader.model_validate(workspace, from_attributes=True)


@workspace_router.get("/list")
async def get_workspaces(
    user: public.User = Depends(get_logged_user_in_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> list[WorkspaceHeader]:
    workspace_service.get_all_by_participant(user)


@workspace_router.get("/{workspace_id}")
async def get_workspace_(
    user: public.User = Depends(get_logged_user_in_workspace),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> Workspace:
    return Workspace.model_validate(
        await workspace_service.get_full(workspace), from_attributes=True
    )


@workspace_router.delete("/{workspace_id}")
async def delete_workspace(
    user: public.User = Depends(get_workspace_admin),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> None:
    await workspace_service.delete_workspace(workspace)


@workspace_router.post("/{workspace_id}/user/{user_id}")
async def add_user(
    user: public.User = Depends(get_workspace_admin),
    user_to_add: public.User = Depends(get_user),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> None:
    try:
        await workspace_service.add_user(workspace, user_to_add)
    except UserAlreadyInWorkspaceError:
        raise user_already_in_workspace


@workspace_router.delete("/{workspace_id}/user/{user_id}")
async def delete_user(
    user: public.User = Depends(get_workspace_admin),
    user_to_delete: int = Depends(get_user),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> None:
    try:
        await workspace_service.delete_user(workspace, user_to_delete)
    except UserNotInWorkspaceError:
        raise user_not_in_workspace


@workspace_router.post("/{workspace_id}/template")
async def add_template(
    template_create: TemplateCreate,
    user: public.User = Depends(get_logged_user_in_workspace),
    workspace: public.Workspace = Depends(get_workspace),
    template_service: TemplateService = Depends(get_template_service),
) -> TemplateHeader:
    template = await template_service.create_template(workspace, template_create, user)

    return TemplateHeader.model_validate(template, from_attributes=True)


@workspace_router.get("/{workspace_id}/templates")
async def get_templates_list(
    user: public.User = Depends(get_logged_user_in_workspace),
    workspace: public.Workspace = Depends(get_workspace),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> list[TemplateHeader]:
    return validate_ta(
        list[TemplateHeader], await workspace_service.get_templates(workspace)
    )


@workspace_router.delete("/{workspace_id}/template/{template_id}")
async def delete_template(
    user: public.User = Depends(get_template_author_or_admin),
    template: public.Template = Depends(get_template),
    template_service: TemplateService = Depends(get_template_service),
) -> None:
    await template_service.delete_template(template)


@workspace_router.put("/{workspace_id}/template/{template_id}")
async def update_template(
    user: public.User = Depends(get_template_author_or_admin),
    template: public.Template = Depends(get_template),
    template_service: TemplateService = Depends(get_template_service),
) -> TemplateHeader:
    pass  # TODO
