from typing import Any, Iterable, Protocol, TypeVar
from sqlalchemy import MetaData, Sequence, delete, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from models.base import BaseIdModel

IdModelT = TypeVar("IdModelT", bound=BaseIdModel)
IdT = TypeVar("IdT", contravariant=True)


class Repository(Protocol[IdModelT, IdT]):
    async def get(self, id: IdT) -> IdModelT | None: ...

    async def add(self, item: IdModelT) -> None: ...

    async def update(self, item: IdModelT, items: dict[str, Any]) -> None: ...

    async def delete(self, item: IdModelT) -> None: ...


class AlchemyIdRepository(Repository[IdModelT, IdT]):
    alchemy_model: type[IdModelT]  # class var
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: IdT) -> IdModelT | None:
        stmt = select(self.alchemy_model).where(self.alchemy_model.id == id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_with_ids(self, ids: Iterable[IdT]) -> list[IdModelT]:
        stmt = select(self.alchemy_model).where(self.alchemy_model.id.in_(ids))
        return list((await self.session.execute(stmt)).scalars().all())

    async def add(self, item: IdModelT) -> None:
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)

    async def add_all(self, items: Iterable[IdModelT]) -> None:
        self.session.add_all(items)
        await self.session.flush()

    async def update(self, item: IdModelT, items: dict[str, Any]) -> None:
        stmt = (
            update(self.alchemy_model)
            .where(self.alchemy_model.id == item.id)
            .values(**items)
        )
        await self.session.execute(stmt)

    async def delete(self, item: IdModelT) -> None:
        await self.session.delete(item)
        await self.session.flush()

    async def exists_with_id(self, id: IdT) -> bool:
        stmt = select(self.alchemy_model.id).where(self.alchemy_model.id == id)
        return (await self.session.execute(stmt)).first() is not None

    async def exists_with_id_all(self, ids: Iterable[IdT]) -> bool:
        ids_set = set(ids)
        stmt = select(count(self.alchemy_model.id)).where(
            self.alchemy_model.id.in_(ids_set)
        )
        return (await self.session.execute(stmt)).scalar_one() == len(ids_set)
