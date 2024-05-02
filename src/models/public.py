from typing import Callable, TypeAlias, cast
from sqlalchemy import ForeignKey, Table, Column
from .base import BaseIdModel, Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import false


user_workspace = Table(
    "user_workspace",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("workspace_id", ForeignKey("workspace.id"), primary_key=True),
)


class Workspace(BaseIdModel):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str]
    description: Mapped[str | None]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())

    creator: Mapped["User"] = relationship(foreign_keys=[creator_id])
    admin: Mapped["User"] = relationship(foreign_keys=[admin_id])
    users: Mapped[list["User"]] = relationship(
        secondary=user_workspace, back_populates="workspaces"
    )
    templates: Mapped[list["Template"]] = relationship()


class User(BaseIdModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    email: Mapped[str]
    display_name: Mapped[str]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())
    password_hash: Mapped[str]

    workspaces: Mapped[list[Workspace]] = relationship(
        secondary=user_workspace, back_populates="users"
    )


class Template(BaseIdModel):
    __tablename__ = "template"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    workspace_id: Mapped[int] = mapped_column(ForeignKey(Workspace.id))
    name: Mapped[str]
    description: Mapped[str | None]
    latex: Mapped[str | None]
    lua_example: Mapped[str | None]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())

    workspace: Mapped[Workspace] = relationship(back_populates="templates")
    tickets_sets: Mapped[list["TicketsSet"]] = relationship()


class TicketsSet(BaseIdModel):
    __tablename__ = "tickets_set"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    template_id: Mapped[int] = mapped_column(ForeignKey(Template.id))
    name: Mapped[str]
    description: Mapped[str | None]
    lua: Mapped[str | None]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())

    author: Mapped[User] = relationship()
    template: Mapped[Template] = relationship(back_populates="tickets_sets")

    @property
    def s3_id(self) -> str:
        return f"{self.author_id}/{self.id}"
