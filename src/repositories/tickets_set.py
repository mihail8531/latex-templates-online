from dataclasses import dataclass
from repositories.repository import Repository
from settings import settings
from .alchemy import AlchemyIdRepository
from .s3 import S3Repository
from models.public import TicketsSet


class TicketsSetRepository(AlchemyIdRepository[TicketsSet, int]):
    pass


class TicketsSetFileRepository(S3Repository):
    bucket_name = settings.BUCKET_NAME
    url_expires_time = settings.URL_EXPIRES_TIME
