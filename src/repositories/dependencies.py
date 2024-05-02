from functools import cache
from typing import Callable, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from .alchemy import AlchemyIdRepository
from .s3 import S3Repository
from s3.session import S3ServiceResource, get_s3_client

AlchemyRepositoryT = TypeVar("AlchemyRepositoryT", bound=AlchemyIdRepository)
S3RepositoryT = TypeVar("S3RepositoryT", bound=S3Repository)


@cache
def get_alchemy_repository(
    repository_type: type[AlchemyRepositoryT],
) -> Callable[..., AlchemyRepositoryT]:
    def get_alchemy_repository_dependency(
        session: AsyncSession = Depends(get_session),
    ) -> AlchemyRepositoryT:
        return repository_type(session)

    return get_alchemy_repository_dependency


@cache
def get_s3_repository(
    repository_type: type[S3RepositoryT],
) -> Callable[..., S3RepositoryT]:
    def get_s3_repository_dependency(
        s3_client: S3ServiceResource = Depends(get_s3_client),
    ) -> S3RepositoryT:
        return repository_type(s3_client)

    return get_s3_repository_dependency
