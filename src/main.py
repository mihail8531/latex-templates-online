from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes.pages import pages_router
from settings import settings

app = FastAPI(title="Latex templates online", debug=settings.DEBUG)
app.mount("/static", StaticFiles(directory=settings.STATIC_PATH))
app.include_router(pages_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=settings.PORT,
        host=settings.HOST,
        reload=True
    )
