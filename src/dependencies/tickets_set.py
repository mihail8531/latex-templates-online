from fastapi import Depends
from repositories.dependencies import get_alchemy_repository
from repositories.dependencies import get_s3_repository
from repositories.s3 import S3Repository
from repositories.tickets_set import TicketsSetFileRepository, TicketsSetRepository
from services.tickets_set import TicketsSetService


def get_tickets_set_service(
    tickets_set_file_repository: TicketsSetFileRepository = Depends(
        get_s3_repository(TicketsSetFileRepository)
    ),
    tickets_set_repository: TicketsSetRepository = Depends(
        get_alchemy_repository(TicketsSetRepository)
    ),
) -> TicketsSetService:
    return TicketsSetService(tickets_set_file_repository, tickets_set_repository)
