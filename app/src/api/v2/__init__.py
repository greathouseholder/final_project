from fastapi import APIRouter

from .routers.collections import router as collections_router
from .routers.documents import router as documents_router
from .routers.rag import router as rag_router

v2_router = APIRouter(prefix="/v2")
v2_router.include_router(collections_router)
v2_router.include_router(documents_router)
v2_router.include_router(rag_router)

__all__ = ("v2_router",)
