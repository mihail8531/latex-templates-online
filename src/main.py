from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes.auth import auth_router
from routes.user import user_router
from routes.workspace import workspace_router
from settings import settings

app = FastAPI(title="Latex templates online", debug=settings.DEBUG)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workspace_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=settings.PORT,
        host=settings.HOST,
        reload=True
    )
