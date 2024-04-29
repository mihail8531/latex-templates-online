from fastapi import Depends
from models import public
from repositories.dependencies import get_alchemy_repository
from repositories.template import TemplateRepository
from services.template import TemplateNotFound, TemplateService
from services.workspace import WorkspaceService
from .workspace import (
    get_logged_user_in_workspace,
    get_workspace,
    get_workspace_service,
)
from exceptions.template import template_not_found
from exceptions.workspace import operation_not_permitted


def get_template_service(
    template_repository: TemplateRepository = Depends(
        get_alchemy_repository(TemplateRepository)
    ),
):
    return TemplateService(template_repository)


async def get_template(
    template_id: int,
    user: public.User = Depends(get_logged_user_in_workspace),
    template_service: TemplateService = Depends(get_template_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> public.Template:
    try:
        template = await template_service.get(template_id)
    except TemplateNotFound:
        raise template_not_found
    if not workspace_service.have_template(template):
        raise template_service
    return template


def get_template_author_or_admin(
    user: public.User = Depends(get_logged_user_in_workspace),
    workspace: public.Workspace = Depends(get_workspace),
    template: public.Template = Depends(get_template),
    template_service: TemplateService = Depends(get_template_service),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
) -> public.User:
    if not (
        workspace_service.is_user_admin(workspace, user)
        or template_service.is_user_template_author(template, user)
    ):
        raise operation_not_permitted
    return user
