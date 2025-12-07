from fastapi import APIRouter
from .routers.admin import admin_router
from .routers.rag import rag_router
from .routers.search import search_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(admin_router)
v1_router.include_router(rag_router)
v1_router.include_router(search_router)

__all__ = ("v1_router",)
