import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi import status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import secrets


from routes.auth import auth_router
from routes.user import user_router
from routes.workspace import workspace_router
from services.compiler.compiler import CompilersStorage
from services.compiler.texlive_compilers import LuaLatexCompiler
from settings import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.compilers_storage = CompilersStorage()
    await app.state.compilers_storage.register_compiler(LuaLatexCompiler())
    yield


app = FastAPI(
    title="Latex templates online",
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
docs_security = HTTPBasic(
    description="Введите пароль и логин для просмотра документации"
)


def get_current_username(credentials: HTTPBasicCredentials = Depends(docs_security)):
    correct_username = secrets.compare_digest(
        credentials.username, settings.DOCS_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.DOCS_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workspace_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=settings.PORT, host=settings.HOST, reload=settings.DEBUG
    )
