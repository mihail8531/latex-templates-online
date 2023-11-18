from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import DeclarativeBase

from .user import User


class Data(DeclarativeBase):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    data: Mapped[str]
    creation_datetime: Mapped[datetime] = mapped_column(server_default=func.now())
    creator_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    last_editor_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    last_edit_datetime: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted: Mapped[bool] = mapped_column(server_default="f")
