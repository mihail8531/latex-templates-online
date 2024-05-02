from io import BytesIO, StringIO
from models import public
from repositories.repository import File
from repositories.tickets_set import TicketsSetFileRepository, TicketsSetRepository
from schemas.tickets_set import TicketsSetCreate
from services.compiler.compiler import CompilerType, CompilersStorage
from services.compiler.models import Source


class TicketsSetServiceError(BaseException):
    pass


class TicketsSetFileNotFoundError(TicketsSetServiceError):
    pass


class TicketsSetService:
    def __init__(
        self,
        ticket_set_file_repository: TicketsSetFileRepository,
        ticket_set_repository: TicketsSetRepository,
        compiler_storage: CompilersStorage,
    ) -> None:
        self._ticket_set_file_repository = ticket_set_file_repository
        self._ticket_set_repository = ticket_set_repository
        self._compiler_storage = compiler_storage

    async def get_url(self, tickets_set: public.TicketsSet) -> str:
        url = await self._ticket_set_file_repository.get_download_url(tickets_set.s3_id)
        if url is None:
            raise TicketsSetFileNotFoundError("File not found")
        return url

    async def create(
        self,
        tickets_set_create: TicketsSetCreate,
        template: public.Template,
        user: public.User,
    ) -> public.TicketsSet:
        compiler = self._compiler_storage.get_compiler(CompilerType.lualatex)
        compilation_result = await compiler.compile(
            [
                Source(filename="main.tex", source_file=StringIO(template.latex)),
                Source(
                    filename="data.lua", source_file=StringIO(tickets_set_create.lua)
                ),
            ]
        )
        tickets_set = public.TicketsSet(
            author_id=user.id,
            template_id=template.id,
            name=tickets_set_create.name,
            description=tickets_set_create.description,
            lua=tickets_set_create.lua,
            log=compilation_result.output_log.read(),
        )
        await self._ticket_set_repository.add(tickets_set)
        await self._ticket_set_file_repository.add(
            File(id=tickets_set.s3_id, data=compilation_result.output_file)
        )
        return tickets_set

    async def delete(self, tickets_set: public.TicketsSet) -> None:
        s3_id = tickets_set.s3_id
        await self._ticket_set_repository.delete(tickets_set)
        await self._ticket_set_file_repository.delete(File(id=s3_id, data=BytesIO()))
