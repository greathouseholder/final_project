#файл-инвалид мне просто для образца
from typing import Dict
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot_app import states as st
from . import server_handlers as sh

state_router: Router = Router()

#добавление новой коллекции
@state_router.callback_query(F.data == "add_db")
async def add_collection_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.AddNewcollection.coll_name)
    await callback.answer('')
    await callback.message.answer('Введите название коллекции: ')

@state_router.message(st.AddNewcollection.coll_name)
async def add_collection_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.AddNewcollection.coll_descr)
    await message.answer("Введите описание коллекции: ")

@state_router.message(st.AddNewcollection.coll_descr)
async def add_collection(message: Message, state: FSMContext):
    await state.update_data(descr=message.text)
    data: Dict = await state.get_data()
    user_id: int = message.from_user.id
    answer: str = await sh.add_collection_server(user_id, data['name'], data['descr'])
    await message.answer(answer)
    await state.clear()

#удаление коллекции
@state_router.callback_query(F.data == 'delete_db')
async def delete_collection_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.DeleteCollection.coll_name)
    await callback.answer('')
    await callback.message.answer('Введите название коллекции, которую нужно удалить: ')

@state_router.message(st.DeleteCollection.coll_name)
async def delete_collection(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data: Dict = await state.get_data()
    user_id: int = message.from_user.id
    answer: str = await sh.delete_collection_server(data['name'].strip(), user_id)
    if answer == 'success':
        await message.answer('Коллекция успешно удалена')
    else:
        await message.answer(f'Ошибка: {answer}')
    await state.clear()
