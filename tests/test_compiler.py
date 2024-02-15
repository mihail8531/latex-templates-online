import re
from io import StringIO

import pytest

from compiler import Compiler, CompilersStorage, LuaLatexCompiler, Source #type: ignore[import-not-found]


@pytest.mark.asyncio
async def test_lualatex_compiler() -> None:
    compiler = LuaLatexCompiler()
    await compiler.check_requirements()
    with open("tests/tex_files/hello_world.tex", "r") as hello_world_tex:
        sources = [Source("main.tex", StringIO(hello_world_tex.read()))]
    result = await compiler.compile(sources)

    output_pdf_file = result.output_file.read()
    # with open("output.pdf", 'wb') as f:
    #     f.write(output_pdf_file)
    # with open("output.log", 'w') as f:
    #     f.write(result.output_log.read())
    assert len(output_pdf_file) > 0
    assert re.search(r"%PDF-.+\n", output_pdf_file.decode(errors="ignore")) is not None


@pytest.mark.asyncio
async def test_compilers_storage() -> None:
    storage = CompilersStorage()
    compiler_1: Compiler = LuaLatexCompiler()
    await storage.register_compiler(compiler_1)
    assert storage.get_compiler(compiler_1.__compiler_type__) is compiler_1
