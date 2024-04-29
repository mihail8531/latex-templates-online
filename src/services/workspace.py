from models import public
from repositories.template import TemplateRepository
from repositories.workspace import WorkspaceRepository
from schemas.template import TemplateCreate
from schemas.workspace import WorkspaceCreate
from services.user import UserNotFoundError, UserService


class WorkspaceServiceError(BaseException):
    pass


class OperationNotPermittedError(WorkspaceServiceError):
    pass


class WorkspaceNotFoundError(WorkspaceServiceError):
    pass


class UserAlreadyInWorkspaceError(WorkspaceServiceError):
    pass


class UserNotInWorkspaceError(WorkspaceServiceError):
    pass


class WorkspaceService:
    def __init__(
        self,
        workspace_repository: WorkspaceRepository,
    ) -> None:
        self._workspace_repository = workspace_repository

    async def create(
        self, workspace_create: WorkspaceCreate, creator: public.User
    ) -> public.Workspace:
        workspace = public.Workspace(
            creator_id=creator.id,
            admin_id=creator.id,
            name=workspace_create.name,
            description=workspace_create.description,
        )
        await self._workspace_repository.add(workspace)
        return workspace

    async def delete_workspace(self, workspace: public.Workspace) -> None:
        if not self.is_user_admin:
            raise OperationNotPermittedError("Only admin can remove a workspace")
        await self._workspace_repository.delete(workspace)

    async def get(
        self, workspace_id: int, user: public.User | None = None
    ) -> public.Workspace:
        workspace = await self._workspace_repository.get(workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundError(
                f"Workspace with given id not found ({workspace_id})"
            )
        if user is None:
            return workspace
        if not await self.is_user_in_workspace(workspace, user):
            raise OperationNotPermittedError("User can't see this workspace")
        return workspace

    async def get_all_by_participant(self, user: public.User) -> list[public.Workspace]:
        return await self._workspace_repository.get_all_by_participant_id(user.id)

    async def get_full(self, workspace: public.Workspace) -> public.Workspace:
        return await self._workspace_repository.get_full(workspace)

    async def ensure_have_admin_rights(
        self, workspace: public.Workspace, user: public.User | None
    ) -> None:
        if user is not None and not self.is_user_admin(workspace, user):
            raise OperationNotPermittedError(
                "User must be an admin to add users to workspace"
            )

    async def is_user_in_workspace(
        self, workspace: public.Workspace, user: public.User
    ) -> bool:
        workspace_users = await self._workspace_repository.get_users(workspace)
        return user.id in [user.id for user in workspace_users]

    async def add_user(
        self,
        workspace: public.Workspace,
        user_to_add: public.User,
    ) -> None:
        if await self.is_user_in_workspace(workspace, user_to_add):
            raise UserAlreadyInWorkspaceError("User already in workspace")
        await self._workspace_repository.add_user(workspace, user_to_add)

    async def delete_user(
        self,
        workspace: public.Workspace,
        user_to_delete: public.User,
    ) -> None:
        if not await self.is_user_in_workspace(workspace, user_to_delete):
            raise UserNotInWorkspaceError("User not in given workspace")
        await self._workspace_repository.delete_user(workspace, user_to_delete)

    async def get_templates(self, workspace: public.Workspace) -> list[public.Template]:
        return await self._workspace_repository.get_templates(workspace)

    async def have_template(self, template: public.Template) -> bool:
        return template.id in await self.get_templates()

    def is_user_admin(self, workspace: public.Workspace, user: public.User) -> bool:
        return workspace.admin_id == user.id
