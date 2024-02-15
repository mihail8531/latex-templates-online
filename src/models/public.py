from sqlalchemy import ForeignKey
from .base import BaseIdModel
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import false


class Workspace(BaseIdModel):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column("User.id")
    admin_id: Mapped[int] = mapped_column("User.id")
    name: Mapped[str]
    description: Mapped[str | None]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())
    deleted: Mapped[bool] = mapped_column(server_default=false())


class User(BaseIdModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    display_name: Mapped[str]
    name: Mapped[str | None]
    surname: Mapped[str | None]
    patronymic: Mapped[str | None]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())
    password_hash: Mapped[str]
    deleted: Mapped[bool] = mapped_column(server_default=false())

    workspaces: Mapped[list[Workspace]] = relationship()


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
    edit_timestamp: Mapped[datetime] = mapped_column(server_default=now())
    deleted: Mapped[bool] = mapped_column(server_default=false())


class TicketsSet(BaseIdModel):
    __tablename__ = "tickets_set"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    template_id: Mapped[int] = mapped_column(ForeignKey(Template.id))
    name: Mapped[str]
    description: Mapped[str | None]
    lua: Mapped[str | None]
    creation_timestamp: Mapped[datetime] = mapped_column(server_default=now())
    edit_timestamp: Mapped[datetime] = mapped_column(server_default=now())
    deleted: Mapped[bool] = mapped_column(server_default=false())
