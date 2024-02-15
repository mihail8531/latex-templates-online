from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped


class BaseIdModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[Any]
