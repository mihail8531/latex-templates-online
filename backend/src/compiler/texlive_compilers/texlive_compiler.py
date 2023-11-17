from aiofiles import open
import os
from typing import Sequence, Any
from abc import ABC, abstractmethod
from utils import async_shutil_which
import shutil
import asyncio
from ..compiler import Compiler, Source
from ..exceptions import CompilerRequierementsNotSatisfied



class TexliveCompiler(Compiler, ABC):

    @abstractmethod
    async def _get_compiler_executable_name(self) -> str:
        ...

    async def _prepare_enviroment(self, sources: Sequence[Source], directory: str) -> str | None:
        """
        saves source files to given directory
        returns main.tex file path or None if main.tex file not found
        """
        main_tex_path: str | None = None
        for source in sources:
            path = os.path.join(directory, source.filename)
            if source.filename.lower() == "main.tex":
                main_tex_path = path
            async with open(path, "w") as f:
                await f.write(source.source_file.read())
        return main_tex_path

    async def check_requirements(self) -> None:
        compiler_executable_name = await self._get_compiler_executable_name()
        if await async_shutil_which(compiler_executable_name) is None:
            raise CompilerRequierementsNotSatisfied(
                f"Compiler executable name {compiler_executable_name} not found!"
            )
