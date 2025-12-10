from fastapi import APIRouter

from .routers.collections import collections_router
from .routers.conversations import conversations_router

v2_router = APIRouter(prefix="/v2")
v2_router.include_router(collections_router)
v2_router.include_router(conversations_router)

__all__ = ("v2_router",)
