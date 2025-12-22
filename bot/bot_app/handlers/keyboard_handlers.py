#для настройки работы кнопок навигационных клавиатур
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot_app import keyboards as kb

keyboard_router: Router = Router()

@keyboard_router.callback_query(F.data == 'collections')
async def user_panel(callback: CallbackQuery) -> None:
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.collections_menu)

@keyboard_router.callback_query(F.data == 'main_menu')
async def open_panels(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_text('Выберите действие', reply_markup=kb.main_menu)

#навигация для умной клавиатуры:
@keyboard_router.callback_query(F.data == "current_page")
async def current_page(callback: CallbackQuery):
    await callback.answer('')

#для коллекций
@keyboard_router.callback_query(F.data.startswith("page_"))
async def go_to_page(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if "documents" in data:
        documents = data.get("documents", [])
        current_page = int(callback.data.split("_")[1])
        keyboard = kb.create_pagination_keyboard(documents, "document", current_page)
        await callback.message.edit_text('Выберите документ:', reply_markup=keyboard)
    elif "collections" in data:
        collections = data.get("collections", [])
        current_page = int(callback.data.split("_")[1])
        keyboard = kb.create_pagination_keyboard(collections, "collection", current_page)
        await callback.message.edit_text('Выберите коллекцию:', reply_markup=keyboard)

@keyboard_router.callback_query(F.data == 'pay')
async def handle_pay(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Хотите ли Вы оплатить подписку", reply_markup=kb.payment_keyboard)