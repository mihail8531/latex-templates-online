from repositories.template import TemplateRepository
import models.public as public
from schemas.template import TemplateCreate
from services.workspace import WorkspaceService


class TemplateServiceError(BaseException):
    pass


class TemplateNotFound(TemplateServiceError):
    pass


class TemplateService:
    def __init__(self, template_repository: TemplateRepository) -> None:
        self._template_repository = template_repository

    async def get(self, template_id: int) -> public.Template:
        template = await self._template_repository.get(template_id)
        if template is None:
            raise TemplateNotFound
        return template

    async def create_template(
        self,
        workspace: public.Workspace,
        template_create: TemplateCreate,
        author: public.User,
    ) -> public.Template:
        template = public.Template(
            author_id=author.id,
            workspace_id=workspace.id,
            name=template_create.name,
            description=template_create.description,
            latex=template_create.latex,
            lua_example=template_create.lua_example,
        )
        await self._template_repository.add(template)
        return template

    async def delete_template(
        self,
        template: public.Template,
    ) -> None:
        await self._template_repository.delete(template)

    def is_user_template_author(
        self, template: public.Template, user: public.User
    ) -> bool:
        return template.author_id == user.id
