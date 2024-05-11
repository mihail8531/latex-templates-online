import aiofiles
import asyncio
from typing import Sequence, cast
import os
from ..models import CompilationResult, Source
from ..compiler import CompilerType
from .texlive_compiler import TexliveCompiler
from .exceptions import CompilationFailedError
from utils import async_os_path_exists
from io import BytesIO, StringIO


class TexliveLualatexCompiler(TexliveCompiler):
    __compiler_type__ = CompilerType.lualatex

    async def _get_compiler_executable_name(self) -> str:
        return "lualatex"

    async def compile(self, sources: Sequence[Source]) -> CompilationResult:
        async with aiofiles.tempfile.TemporaryDirectory() as tempdir:
            main_tex_path = await self._prepare_environment(sources, cast(str, tempdir))
            if main_tex_path is None:
                raise CompilationFailedError("main.tex not found")
            with open(os.devnull, 'wb+') as devnull:
                process = await asyncio.create_subprocess_shell(
                    " ".join(
                        [
                            "cd",
                            tempdir,
                            "&&" "lualatex",
                            "--interaction=nonstopmode",
                            "--shell-escape",
                            "--no-socket",
                            "--output-format=pdf",
                            main_tex_path,
                        ]
                    ),
                    stdout=devnull,
                    stderr=devnull,
                )
                await process.communicate()
            output_log_file_path = os.path.join(tempdir, "main.log")
            output_pdf_file_path = os.path.join(tempdir, "main.pdf")
            if await async_os_path_exists(output_log_file_path):
                async with aiofiles.open(output_log_file_path, "r") as output_log_file:
                    output_log = StringIO(await output_log_file.read())
            else:
                output_log = StringIO("Compilation log not found")
            # if process.returncode != 0:
            #     raise CompilationFailed(output_log.read())
            if not await async_os_path_exists(output_pdf_file_path):
                raise CompilationFailedError(output_log.read())
            try:
                async with aiofiles.open(output_pdf_file_path, "rb") as output_pdf_file:
                    output_file = BytesIO(await output_pdf_file.read())
            except OSError as e:
                raise CompilationFailedError(f"{e}\n{output_log.read()}")
        return CompilationResult(output_file=output_file, output_log=output_log)