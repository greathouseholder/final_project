from typing import Dict, List
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from . import server_handlers as sh
import bot_app.keyboards as kb
from bot_app import states as st
from config import DOCUMENTS_EXAMPLE

documents_router: Router = Router()

@documents_router.callback_query(st.StateAndCallbackFilter("view_docs", st.ViewCollections.view))
async def view_docs(callback: CallbackQuery, state: FSMContext):
    user_id: int = callback.from_user.id
    data = await state.get_data()
    coll_id: int = data.get("id")
    #docs = await sh.view_docs(user_id, coll_id) #не тест
    docs: Dict = DOCUMENTS_EXAMPLE #тест
    await state.update_data(documents=docs)
    if len(docs) == 0:
        await callback.answer()
        await callback.message.answer("Список документов пуст")
        await state.clear()
    elif "error" in docs[0]:
        await callback.answer()
        await callback.message.answer(docs[0]["error"])
        await state.clear()
    else:
        keyboard = kb.create_pagination_keyboard(docs, "document")
        await state.update_data(docs=docs, current_page=0)
        await callback.message.edit_text('Выберите документ:', reply_markup=keyboard)