from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class BaseIdModel(Base):
    __abstract__ = True

    id: Mapped[Any]
