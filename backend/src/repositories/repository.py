from typing import Protocol, Any

from pydantic import BaseModel

from utils.typevars import IdT, ObjectT


class BaseRepository(Protocol[IdT, ObjectT]):
    async def get_by_id(self, id: IdT) -> ObjectT:
        raise NotImplementedError()

    async def create(self, schema: BaseModel) -> ObjectT:
        raise NotImplementedError()

    async def patch(self, id: IdT, schema: BaseModel) -> ObjectT:
        raise NotImplementedError()

    async def patch_attr(self, id: IdT, attr: str, value: Any) -> ObjectT:
        raise NotImplementedError()

    async def put(self, id: IdT, schema: BaseModel) -> ObjectT:
        raise NotImplementedError()

    async def remove_by_id(self, id: IdT) -> None:
        raise NotImplementedError()
