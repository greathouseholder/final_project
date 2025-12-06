from fastapi import APIRouter

from .di import container
from .v1 import v1_router

routers = APIRouter(prefix="/api")
routers.include_router(v1_router)

__all__ = ("routers", "container")
