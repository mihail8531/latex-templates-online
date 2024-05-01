from dataclasses import dataclass
from repositories.repository import Repository
from .alchemy import AlchemyIdRepository
from .s3 import S3Repository
from models.public import TicketsSet


class TicketsSetRepository(AlchemyIdRepository[TicketsSet, int]):
    pass


class TicketsSetFileRepository(S3Repository):
    pass
