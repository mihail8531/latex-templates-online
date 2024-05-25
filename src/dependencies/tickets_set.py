from fastapi import Depends, FastAPI
from dependencies.compiler import get_compilers_storage
from models import public
from repositories.dependencies import get_alchemy_repository
from repositories.dependencies import get_s3_repository
from repositories.tickets_set import (
    TicketsSetFileRepository,
    TicketsSetRepository,
    TicketsSetSourceFileRepository,
)
from services.compiler.compiler import CompilersStorage
from services.tickets_set import TicketsSetNotFoundError, TicketsSetService
from exceptions.tickets_set import tickets_set_not_found


def get_tickets_set_service(
    tickets_set_file_repository: TicketsSetFileRepository = Depends(
        get_s3_repository(TicketsSetFileRepository)
    ),
    tickets_set_repository: TicketsSetRepository = Depends(
        get_alchemy_repository(TicketsSetRepository)
    ),
    tickets_set_source_file_repository: TicketsSetSourceFileRepository = Depends(
        get_s3_repository(TicketsSetSourceFileRepository)
    ),
    compilers_storage: CompilersStorage = Depends(get_compilers_storage),
) -> TicketsSetService:
    return TicketsSetService(
        tickets_set_file_repository,
        tickets_set_repository,
        tickets_set_source_file_repository,
        compilers_storage,
    )


async def get_tickets_set(
    tickets_set_id: int,
    tickets_set_service: TicketsSetService = Depends(get_tickets_set_service),
) -> public.TicketsSet:
    try:
        return await tickets_set_service.get_tickets_set(tickets_set_id)
    except TicketsSetNotFoundError:
        raise tickets_set_not_found
