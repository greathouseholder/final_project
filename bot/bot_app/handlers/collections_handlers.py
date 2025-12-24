#действия с коллекциями
from typing import Dict, List
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from uuid import UUID

from . import server_handlers as sh
import bot_app.keyboards as kb
from bot_app import states as st
from config import COLLECTION_EXAMPLE #коллекция для тестирования

collections_router: Router = Router()

#кнопка добавления коллекции
@collections_router.callback_query(F.data == "add_db")
async def add_collection(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.AddNewcollection.coll_name)
    await callback.answer()
    await callback.message.answer("Введите название коллекции: ", reply_markup=kb.cancel_button_keyboard)

#откат к меню коллекций
@collections_router.callback_query(st.StateAndCallbackFilter("cancel", st.AddNewcollection.coll_descr))
@collections_router.callback_query(st.StateAndCallbackFilter("cancel", st.AddNewcollection.coll_name))
@collections_router.callback_query(st.StateAndCallbackFilter("cancel", st.UpdateCollection.coll_name))
@collections_router.callback_query(st.StateAndCallbackFilter("cancel", st.UpdateCollection.coll_desc))
@collections_router.callback_query(st.StateAndCallbackFilter("cancel", st.UpdateCollection.is_public))
async def cancel_add_coll(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text('Выберите действие', reply_markup=kb.collections_menu)

#сохранение названия колекции и запрос описания
@collections_router.message(st.AddNewcollection.coll_name)
async def set_coll_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.AddNewcollection.coll_descr)
    await message.answer("Введите описание коллекции: ", reply_markup=kb.cancel_button_keyboard)

#сохранение описания и запрос личное непубличное
@collections_router.message(st.AddNewcollection.coll_descr)
async def set_coll_descr(message: Message, state: FSMContext):
    await state.update_data(descr=message.text)
    await state.set_state(st.AddNewcollection.is_public)
    await message.answer("Приватная или публичная коллекция?", reply_markup=kb.is_public_keyboard)

#добавление
@collections_router.callback_query(st.StateAndCallbackStartsWithFilter('public_', st.AddNewcollection.is_public))
async def set_is_public(callback: CallbackQuery, state: FSMContext):
    is_public: bool = int(callback.data[-1])
    data: Dict = await state.get_data()
    user_id: int = callback.from_user.id
    coll_name: str = data.get("name", "Без имени")
    coll_descr: str = data.get("descr", "Без описания")
    await callback.answer()
    response: Dict = await sh.add_collection_server(user_id, coll_name, coll_descr, is_public)
    await callback.message.answer(response)
    await state.clear()

#выбрать коллекцию для действий с коллекциями
@collections_router.callback_query(F.data == "collections_actions")
async def collections_actions(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.ViewCollections.view)
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
        keyboard = kb.create_pagination_keyboard(collections, "c")
        await state.update_data(collections=collections, current_page=0)
        await callback.message.edit_text('Выберите коллекцию:', reply_markup=keyboard)

@collections_router.callback_query(st.StateAndCallbackStartsWithFilter("c:",
                                                                       st.ViewCollections.view))
async def other_actions(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=UUID(callback.data.split(":")[1]))
    await callback.answer()
    await callback.message.answer("Выберите действие: ", reply_markup=kb.collections_actions_menu)

#удалить коллекцию
@collections_router.callback_query(st.StateAndCallbackFilter("delete_db", st.ViewCollections.view))
async def delete_db(callback: CallbackQuery, state: FSMContext):
    data: Dict = await state.get_data()
    coll_id: UUID = data.get("id")
    user_id: int = callback.from_user.id
    '''response = await sh.delete_collection_server(coll_id, user_id)
    await callback.answer()
    if response == "success":
        await callback.message.answer(f"Коллекция успешно удалена")
    else:
        await callback.message.answer(f"Ошибка: {response}")'''
    await callback.message.answer(f"Удалена коллекция id={coll_id}")
    await state.clear()

#изменить коллекцию
@collections_router.callback_query(F.data == 'update_coll')
async def update_coll_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(st.UpdateCollection.coll_name)
    await callback.message.answer("Введите новое название коллекции:",
                                  reply_markup=kb.cancel_button_keyboard)
    
@collections_router.message(st.UpdateCollection.coll_name)
async def update_coll_desc(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.UpdateCollection.is_public)
    await message.answer("Хотите ли Вы, чтобы коллекция была приватная или публичная?",
                                  reply_markup=kb.is_public_keyboard)

@collections_router.callback_query(st.StateAndCallbackStartsWithFilter('public_',
                                                                       st.UpdateCollection.is_public))
async def update_coll_is_public(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_public=callback.data[-1])
    await callback.answer()
    await state.set_state(st.UpdateCollection.coll_desc)
    await callback.message.answer("Введите новое описание коллекции", reply_markup=kb.cancel_button_keyboard)

@collections_router.message(st.UpdateCollection.coll_desc)
async def update_coll(message: Message, state: FSMContext):
    desc = message.text
    data = await state.get_data()
    name = data.get('name')
    coll_id: UUID = data.get('id')
    is_public: bool = data.get('is_public')
    user_id: int = message.from_user.id
    response = await sh.update_coll(user_id, coll_id, name, is_public, desc)
    if 'detail' in response:
        await message.answer(f"Ошибка: {response.get('detail')}")
    else:
        await message.answer("Коллекция успешно изменена")
