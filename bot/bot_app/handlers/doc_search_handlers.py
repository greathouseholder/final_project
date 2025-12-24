#поиск документа в коллекции
from typing import Dict, List
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from uuid import UUID

from . import server_handlers as sh
from bot_app import states as st
import bot_app.keyboards as kb
#from config import COLLECTION_EXAMPLE #коллекция для тестирования

doc_search_router: Router = Router()

#выбор коллекции
@doc_search_router.callback_query(F.data == 'search')
async def doc_choose_coll(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.DocSearch.choose_coll)
    #collections = COLLECTION_EXAMPLE #тест
    collections: List[Dict[str, str]] = await sh.view_dbs_internal(callback.from_user.id) #не тест
    if len(collections) == 0:
        await callback.answer()
        await callback.message.answer("Список коллекций пуст")
        await state.clear()
    elif "error" in collections[0]:
        await callback.answer()
        await callback.message.answer(collections[0]["error"])
        await state.clear()
    else:
        keyboard = kb.create_pagination_keyboard(collections, "c")
        await state.update_data(collections=collections, current_page=0)
        await callback.message.edit_text('Выберите коллекцию:', reply_markup=keyboard)

#выбор количества источников
@doc_search_router.callback_query(st.StateAndCallbackStartsWithFilter("c:",
                                                                 st.DocSearch.choose_coll))
async def doc_search_choose_number_of_sources(callback: CallbackQuery, state: FSMContext):
    await state.update_data(coll_id=UUID(callback.data.split(':')[1]))
    await state.set_state(st.DocSearch.choose_number_of_sources)
    await callback.message.edit_text(text="Выберите количество источников, которое хотите получить",
                                     reply_markup=kb.number_of_sources)
    
#возврат от выбора количества источников к выбору коллекций
@doc_search_router.callback_query(st.StateAndCallbackFilter("cancel",
                                                                 st.DocSearch.choose_number_of_sources))
async def cancel_doc_search_number_of_sources_choose(callback: CallbackQuery,
                                                     state: FSMContext):
    await state.set_state(st.DocSearch.choose_coll)
    data = await state.get_data()
    collections = data.get("collections", [])
    keyboard = kb.create_pagination_keyboard(collections, "c")
    await callback.message.edit_text('Выберите коллекцию:', reply_markup=keyboard)

#ввод запроса
@doc_search_router.callback_query(st.StateAndCallbackStartsWithFilter("sources_",
                                                                 st.DocSearch.choose_number_of_sources))
async def doc_search_input(callback: CallbackQuery, state: FSMContext):
    await state.update_data(number_of_sources=callback.data[8:])
    await state.set_state(st.DocSearch.input_query)
    await callback.answer('')
    await callback.message.answer('Введите Ваш запрос: ', reply_markup=kb.cancel_button_keyboard)

#возврат от ввода запроса к выбору количества источников
@doc_search_router.callback_query(st.StateAndCallbackFilter("cancel",
                                                            st.DocSearch.input_query))
async def cancel_doc_search_input(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.DocSearch.choose_number_of_sources)
    await callback.message.edit_text(text="Выберите количество источников, которое хотите получить",
                                     reply_markup=kb.number_of_sources)

#отправка запроса на сервер
@doc_search_router.message(st.DocSearch.input_query)
async def search_doc_query(message: Message, state: FSMContext):
    await state.update_data(query=message.text)
    data = await state.get_data()
    query = data.get('query')
    coll_id: UUID = data.get('coll_id')
    user_id = message.from_user.id
    number_of_sources = data.get("number_of_sources", "Не указано")
    response = await sh.search_docs(coll_id, user_id, number_of_sources, query)
    if "detail" in response:
        await message.answer(f"Ошибка: {response['detail']}")
    else:
        await message.answer(f"*{response['title']}*"
                             f"\n \n"
                             f"Название файла: {response['file_name']}\n"
                             f"Размер файла: {response['file_size']} Mb\n"
                             f"Загружен в коллекцию: {response['created_at']}\n"
                             f"Ссылка на источник: {response['metadata']['url']}")
    await state.clear()
