from fastapi import APIRouter
from .login import login_router

partial_router = APIRouter(prefix="/partial")
partial_router.include_router(login_router)
