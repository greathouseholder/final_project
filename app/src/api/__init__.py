from fastapi import APIRouter

from .di import container
from .v2 import v2_router

routers = APIRouter(prefix="/api")
routers.include_router(v2_router)

__all__ = ("routers", "container")
