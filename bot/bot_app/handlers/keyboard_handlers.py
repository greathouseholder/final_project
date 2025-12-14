#для настройки работы кнопок навигационных клавиатур
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot_app import keyboards as kb

keyboard_router: Router = Router()

@keyboard_router.callback_query(F.data == 'user_panel')
async def user_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.user_actions)

@keyboard_router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.admin_actions)

@keyboard_router.callback_query(F.data == 'return')
async def return_to_main_page(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.select_dialogue)

@keyboard_router.callback_query(F.data == 'create_dialogue')
async def create_dialogue(callback: CallbackQuery) -> None:
    await callback.message.answer("Введите название диалога:", reply_markup=kb.back_button_keyboard)
    await callback.answer('')

@keyboard_router.callback_query(F.data == 'panels')
async def open_panels(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите панель', reply_markup=kb.panels)
