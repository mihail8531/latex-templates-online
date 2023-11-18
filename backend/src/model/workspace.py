from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import DeclarativeBase

from .user import User


class Workspace(DeclarativeBase):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    creator_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    admin_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    creation_datetime: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted: Mapped[bool] = mapped_column(server_default="f")
