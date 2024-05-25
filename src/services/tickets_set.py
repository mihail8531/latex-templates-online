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
from schemas.tickets_set import TicketsSet, TicketsSetSource
from services.compiler.compiler import CompilerType, CompilersStorage
from services.compiler.models import Source
from services.compiler.texlive_compilers.exceptions import CompilationFailedError


class TicketsSetServiceError(BaseException):
    pass


class TicketsSetFileNotFoundError(TicketsSetServiceError):
    pass


class CompilationError(TicketsSetServiceError):
    pass


class TicketsSetNotFoundError(TicketsSetServiceError):
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
            tickets_set.s3_id, tickets_set.filename, pdf_show=True
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
        for source_file in source_files:
            source_file.file.seek(0)
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
        filename_map = {source.filename: source for source in source_files}
        await self._tickets_set_repository.add(tickets_set)
        await self._tickets_set_file_repository.add(
            File(id=tickets_set.s3_id, data=compilation_result.output_file)
        )
        await tickets_set.awaitable_attrs.sources
        for source in tickets_set.sources:
            await self._tickets_set_source_file_repository.add(
                File(
                    id=source.s3_id,
                    data=BytesIO(filename_map[source.filename].file.read()),
                )
            )
        return tickets_set

    async def delete(self, tickets_set: public.TicketsSet) -> None:
        s3_id = tickets_set.s3_id
        await self._tickets_set_repository.delete(tickets_set)
        await self._tickets_set_file_repository.delete(File(id=s3_id, data=BytesIO()))

    async def get_tickets_set(self, tickets_set_id: int) -> public.TicketsSet:
        tickets_set = await self._tickets_set_repository.get(tickets_set_id)
        if tickets_set is None:
            raise TicketsSetNotFoundError()
        return tickets_set

    async def get_tickets_set_full(self, tickets_set: public.TicketsSet) -> TicketsSet:
        sources_list = await self._tickets_set_repository.get_sources_list(tickets_set)
        for i, source in enumerate(sources_list):
            if source.filename.endswith(".lua"):
                additional_sources = sources_list[:i] + sources_list[i + 1 :]
                lua_source = sources_list[i]
                break
        else:
            additional_sources = sources_list
            lua_source = None
        additional_sources_schemas = [
            TicketsSetSource(
                filename=s.filename,
                url=await self._tickets_set_source_file_repository.get_download_url(  # type: ignore[arg-type]
                    s.s3_id, s.filename
                ),
            )
            for s in additional_sources
        ]
        return TicketsSet(
            name=tickets_set.name,
            description=tickets_set.description,
            id=tickets_set.id,
            author_id=tickets_set.author_id,
            template_id=tickets_set.template_id,
            creation_timestamp=tickets_set.creation_timestamp,
            pdf_url=await self._tickets_set_file_repository.get_download_url(  # type: ignore[arg-type]
                tickets_set.s3_id, tickets_set.filename, pdf_show=True
            ),
            lua=(
                None
                if lua_source is None
                else str(
                    (
                        await self._tickets_set_source_file_repository.get(  # type: ignore[union-attr]
                            lua_source.s3_id
                        )
                    ).data.read().decode()
                )
            ),
            additional_sources=additional_sources_schemas,
        )
