from aiogram import F, Router
from aiogram.types import  CallbackQuery

from bot_app import keyboards as kb

callback_router: Router = Router()

@callback_router.callback_query(F.data == 'user_panel')
async def user_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.user_actions)

@callback_router.callback_query(F.data == 'admin_panel')
async def user_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.admin_actions)

@callback_router.callback_query(F.data == 'return')
async def user_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите панель', reply_markup=kb.panels)

@callback_router.callback_query(F.data == 'user_query')
async def user_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.answer('Введите запрос:')
