from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import DeclarativeBase

from .template import Template
from .workspace import Workspace


class TemplateWorkspace(DeclarativeBase):
    __tablename__ = "template_workspace"

    template_id: Mapped[int] = mapped_column(ForeignKey(Template.id), primary_key=True)
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(Workspace.id), primary_key=True
    )
