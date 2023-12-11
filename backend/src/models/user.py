from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    superuser: Mapped[bool]
    registration_datetime: Mapped[datetime] = mapped_column(server_default=func.now())
    deleted: Mapped[bool] = mapped_column(server_default="f")
