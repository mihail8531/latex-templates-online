from typing import Any, TypeVar
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    __abstract__ = True


class BaseIdModel(Base):
    __abstract__ = True

    id: Mapped[Any]
    deleted: Mapped[bool]

_T = TypeVar("_T", bound=BaseIdModel)

def filter_deleted(model: _T) -> _T | None:
    if model.deleted:
        return None
    return model

