#действия с коллекциями, самый жирный
from typing import Dict, List
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from . import server_handlers as sh
import bot_app.keyboards as kb
from config import COLLECTION_EXAMPLE #коллекция для тестирования

collections_router: Router = Router()

@collections_router.callback_query(F.data == "add_db")
async def add_collection(callback: CallbackQuery):
    