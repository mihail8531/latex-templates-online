from dataclasses import dataclass
from repositories.repository import Repository
from settings import settings
from .alchemy import AlchemyIdRepository
from .s3 import S3Repository
from models.public import TicketsSet, TicketsSetSource


class TicketsSetRepository(AlchemyIdRepository[TicketsSet, int]):
    alchemy_model = TicketsSet

    async def get_sources_list(self, tickets_set: TicketsSet) -> list[TicketsSetSource]:
        await tickets_set.awaitable_attrs.sources
        return tickets_set.sources


class TicketsSetFileRepository(S3Repository):
    bucket_name = settings.AWS_BUCKET_NAME
    url_expires_time = settings.AWS_URL_EXPIRES_TIME
    outer_endpoint_url_host = settings.AWS_OUTER_ENDPOINT_HOST


class TicketsSetSourceFileRepository(S3Repository):
    bucket_name = settings.AWS_BUCKET_NAME
    url_expires_time = settings.AWS_URL_EXPIRES_TIME
    outer_endpoint_url_host = settings.AWS_OUTER_ENDPOINT_HOST
