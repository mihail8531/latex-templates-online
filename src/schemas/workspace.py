from pydantic import BaseModel
from schemas.user import User
from datetime import datetime


class WorkspaceBase(BaseModel):
    name: str
    description: str
    creation_timestamp: datetime


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceHeader(WorkspaceBase):
    id: int


class Workspace(WorkspaceHeader):
    creator: User
    admin: User
    users: list[User]
