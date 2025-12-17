#отправка rag-запроса
from typing import Dict, List
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
import json

from . import server_handlers as sh
from bot_app import states as st
import bot_app.keyboards as kb
from config import COLLECTION_EXAMPLE #коллекция для тестирования

rag_router: Router = Router()

#выбор коллекции
@rag_router.callback_query(F.data == 'RAG_query')
async def rag_choose_coll(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.InputQuery.choose_coll)
    collections = COLLECTION_EXAMPLE #тест
    #collections: List[Dict[str, str]] = await sh.view_dbs_internal(callback.from_user.id) #не тест
    if len(collections) == 0:
        await callback.answer()
        await callback.message.answer("Список коллекций пуст")
        await state.clear()
    elif "error" in collections[0]:
        await callback.answer()
        await callback.message.answer(collections[0]["error"])
        await state.clear()
    else:
        keyboard = kb.create_pagination_keyboard(collections)
        await state.update_data(collections=collections, current_page=0)
        await callback.message.edit_text('Выберите коллекцию:', reply_markup=keyboard)

#ввод запроса
@rag_router.callback_query(st.StateAndCallbackStartsWithFilter("select_collection:",
                                                                 st.InputQuery.choose_coll))
async def rag_input(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.InputQuery.input_query)
    await state.update_data(coll_id=callback.data[18:])
    await callback.answer('')
    await callback.message.answer('Введите Ваш запрос: ', reply_markup=kb.cancel_button_keyboard)

#возврат от ввода запроса к выбору коллекций
@rag_router.callback_query(st.StateAndCallbackStartsWithFilter("cancel",
                                                                 st.InputQuery.input_query))
async def cancel_rag_input(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.InputQuery.choose_coll)
    data = await state.get_data()
    collections = data.get("collections", [])
    keyboard = kb.create_pagination_keyboard(collections)
    await callback.message.edit_text('Выберите коллекцию:', reply_markup=keyboard)

#отправка запроса на сервер
@rag_router.message(st.InputQuery.input_query)
async def rag_query(message: Message, state: FSMContext):
    await state.update_data(query=message.text)
    data = await state.get_data()
    query = data.get('query')
    coll_id = data.get('coll_id')
    user_id = message.from_user.id
    response, sources = await sh.send_rag(coll_id, user_id, query)
    if "detail" in sources:
        await message.answer(sources.get("detail"))
    else:
        await message.answer(response)
        json_str = json.dumps(sources, indent=2, ensure_ascii=False)
        json_bytes = json_str.encode('utf-8')
        await message.answer_document(
            document=BufferedInputFile(
                file=json_bytes,
                filename="sources.txt"
            ),
            caption="Источники"
        )
    await state.clear()
