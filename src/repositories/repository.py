from dataclasses import dataclass
from io import BytesIO
from typing import Any, Protocol, TypeVar
from sqlalchemy.orm import DeclarativeBase, Mapped
from models.base import BaseIdModel

T = TypeVar("T")
IdT = TypeVar("IdT", contravariant=True)


@dataclass
class File:
    id: str
    data: BytesIO


class Repository(Protocol[T, IdT]):
    async def get(self, id: IdT) -> T | None: ...

    async def add(self, item: T) -> None: ...

    async def update(self, item: T, items: dict[str, Any]) -> None: ...

    async def delete(self, item: T) -> None: ...


