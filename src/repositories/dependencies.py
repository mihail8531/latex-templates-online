from functools import cache
from typing import Callable, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from .alchemy import AlchemyIdRepository

AlchemyRepositoryT = TypeVar("AlchemyRepositoryT", bound=AlchemyIdRepository)


@cache
def get_alchemy_repository(
    repository_type: type[AlchemyRepositoryT],
) -> Callable[..., AlchemyRepositoryT]:
    def get_alchemy_repository_dependency(
        session: AsyncSession = Depends(get_session),
    ) -> AlchemyRepositoryT:
        return repository_type(session)

    return get_alchemy_repository_dependency
