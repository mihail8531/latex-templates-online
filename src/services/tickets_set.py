from io import BytesIO, StringIO, TextIOWrapper
from uuid import uuid4
from fastapi import UploadFile
from models import public
from repositories.repository import File
from repositories.tickets_set import (
    TicketsSetFileRepository,
    TicketsSetRepository,
    TicketsSetSourceFileRepository,
)
from services.compiler.compiler import CompilerType, CompilersStorage
from services.compiler.models import Source
from services.compiler.texlive_compilers.exceptions import CompilationFailedError


class TicketsSetServiceError(BaseException):
    pass


class TicketsSetFileNotFoundError(TicketsSetServiceError):
    pass


class CompilationError(TicketsSetServiceError):
    pass


class TicketsSetService:
    def __init__(
        self,
        tickets_set_file_repository: TicketsSetFileRepository,
        tickets_set_repository: TicketsSetRepository,
        tickets_set_source_file_repository: TicketsSetSourceFileRepository,
        compiler_storage: CompilersStorage,
    ) -> None:
        self._tickets_set_file_repository = tickets_set_file_repository
        self._tickets_set_repository = tickets_set_repository
        self._tickets_set_source_file_repository = tickets_set_source_file_repository
        self._compiler_storage = compiler_storage

    async def get_url(self, tickets_set: public.TicketsSet) -> str:
        url = await self._tickets_set_file_repository.get_download_url(
            tickets_set.s3_id, tickets_set.filename
        )
        if url is None:
            raise TicketsSetFileNotFoundError("File not found")
        return url

    async def create(
        self,
        sources: list[UploadFile],
        name: str,
        description: str | None,
        template: public.Template,
        user: public.User,
    ) -> public.TicketsSet:
        compiler = self._compiler_storage.get_compiler(CompilerType.lualatex)
        # Source(filename="main.tex", source_file=StringIO(template.latex)),
        # Source(
        #     filename="data.lua",
        #     source_file=StringIO(tickets_set_create.lua),
        # ),
        source_files = [
            Source(filename=source.filename or str(uuid4()), file=source.file)
            for source in sources
        ]
        try:
            compilation_result = await compiler.compile(
                [
                    Source(
                        filename="main.tex",
                        file=BytesIO((template.latex or "").encode()),
                    )
                ]
                + source_files
            )
        except CompilationFailedError:
            raise ValueError(str(template.latex))
        tickets_set = public.TicketsSet(
            author_id=user.id,
            template_id=template.id,
            name=name,
            description=description,
            log=compilation_result.output_log.read(),
            sources=[
                public.TicketsSetSource(filename=source.filename)
                for source in source_files
            ],
        )
        await self._tickets_set_repository.add(tickets_set)
        await self._tickets_set_file_repository.add(
            File(id=tickets_set.s3_id, data=compilation_result.output_file)
        )
        return tickets_set

    async def delete(self, tickets_set: public.TicketsSet) -> None:
        s3_id = tickets_set.s3_id
        await self._tickets_set_repository.delete(tickets_set)
        await self._tickets_set_file_repository.delete(File(id=s3_id, data=BytesIO()))
