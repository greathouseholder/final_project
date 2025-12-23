from typing import Dict
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from . import server_handlers as sh
import bot_app.keyboards as kb
from bot_app import states as st
from config import DOCUMENTS_EXAMPLE

documents_router: Router = Router()

#посмотреть документы
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
        await callback.message.edit_text('Вот все документы из коллекции', reply_markup=keyboard)

#открыть меню действий с документом (посмотреть информацию/изменить)
@documents_router.callback_query(st.StateAndCallbackStartsWithFilter("select_document:",
                                                                     st.ViewCollections.view))
async def document_menu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    documents = data.get('documents')
    doc_id: int = callback.data.split(':')[1]
    aim_doc = {
        "document_id": -100,
        "name": "None",
        "collection_id": -100
    }
    for doc in documents:
        if int(doc.get('document_id')) == int(doc_id):
            aim_doc = doc
            break
    await state.update_data(aim_doc=aim_doc)
    await callback.answer()
    await callback.message.edit_text("Выберите действие с документом",
                                     reply_markup=kb.document_actions_keyboard)

#посмотреть информацию о документе
@documents_router.callback_query(F.data == "doc_info")
async def view_doc_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    aim_doc = data.get("aim_doc")
    await callback.answer()
    doc_id: int = int(aim_doc.get('document_id', -1))
    coll_id: int = int(aim_doc.get('collection_id', -1))
    user_id: int = callback.from_user.id
    response = sh.get_doc(user_id, coll_id, doc_id)
    if 'detail' in response:
        await callback.message.answer(f"Ошибка: {response.get('detail')}")
    else:
        metadata = response.get('metadata')
        url = metadata.get('url')
        await callback.message.answer(f"<b> {response.get('title', -1)} </b> \n \n"
                                    f"Название файла: {response.get('file_name', -1)}\n "
                                    f"Размер файла: {response.get('file_size', 'без названия')} Mb\n"
                                    f"Загружен в коллекцию: {response.get('created_at', 'без названия')}\n"
                                    f"Ссылка на источник: {url}\n")
    await state.clear()

#изменение информации о документе: запрос ввода названия
@documents_router.callback_query(F.data == 'update_doc')
async def update_doc_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(st.UpdateDocument.input_name)
    await callback.message.answer("Введите новое название документа:",
                                  reply_markup=kb.cancel_button_keyboard)
    
#запрос ввода описания
@documents_router.message(st.UpdateDocument.input_name)
async def update_doc_desc(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.UpdateDocument.input_desc)
    await message.answer("Введите новое описание: ",
                         reply_markup=kb.cancel_button_keyboard)

#запрос на обновление документа
@documents_router.message(st.UpdateDocument.input_desc)
async def update_doc(message: Message, state: FSMContext):
    data = await state.get_data()
    desc = message.text
    name = data.get("name")
    doc = data.get("aim_doc")
    doc_id = doc.get("document_id")
    coll_id = doc.get("collection_id")
    user_id = message.from_user.id
    response = await sh.update_doc(user_id, coll_id, doc_id, name, desc)
    if 'detail' in response:
        await message.answer(f"Ошибка: {response.get('detail')}")
    else:
        await message.answer("Документ успешно изменён")
    await state.clear()

#добавление документа: запрос ввода названия
@documents_router.callback_query(st.StateAndCallbackFilter("add_doc", st.ViewCollections.view))
async def add_doc_name(callback: CallbackQuery, state: FSMContext):
    data: Dict = await state.get_data()
    coll_id: int = data.get("id", "-1")
    await state.set_state(st.AddDoc.input_name)
    await state.update_data(id=coll_id)
    await callback.message.edit_text("Введите название документа",
                                     reply_markup=kb.cancel_button_keyboard)

#откат к меню выбора действий с коллекцией
@documents_router.callback_query(st.StateAndCallbackFilter("cancel", st.AddDoc.input_name))
@documents_router.callback_query(st.StateAndCallbackFilter("cancel", st.AddDoc.input_desc))
@documents_router.callback_query(st.StateAndCallbackFilter("cancel", st.AddDoc.input_url))
@documents_router.callback_query(st.StateAndCallbackFilter("cancel", st.AddDoc.send_file))
@documents_router.callback_query(st.StateAndCallbackFilter("cancel", st.UpdateDocument.input_name))
@documents_router.callback_query(st.StateAndCallbackFilter("cancel", st.UpdateDocument.input_desc))
async def cancel_add_edit_doc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(st.ViewCollections.view)
    await callback.message.edit_text('Выберите действие', reply_markup=kb.collections_actions_menu)

#запрос ввода описания
@documents_router.message(st.AddDoc.input_name)
async def add_doc_desc(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.AddDoc.input_desc)
    await message.answer("Введите описание документа", reply_markup=kb.cancel_button_keyboard)

#запрос ввода ссылки
@documents_router.message(st.AddDoc.input_desc)
async def add_doc_url(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.set_state(st.AddDoc.input_url)
    await message.answer("Введите url-ссылку на источник", reply_markup=kb.cancel_button_keyboard)

#запрос отправки файла
@documents_router.message(st.AddDoc.input_url)
async def add_doc_file(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(st.AddDoc.send_file)
    await message.answer("Отправьте файл документа в формате .txt")

#запрос на сервер
@documents_router.message(st.AddDoc.send_file)
async def add_doc(message: Message, state: FSMContext):
    data: Dict = await state.get_data()
    coll_id: int = data.get("id", "-1")
    name: str = data.get("name", "Без названия")
    descr: str = data.get("desc", "Без описания")
    url: str = data.get("url", "Без ссылки")
    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    if hasattr(file_bytes, 'read'):
        file_bytes = file_bytes.read()
    filename: str = message.document.file_name
    json: Dict = {
        "telegram_id": message.from_user.id,
        "title": name,
        "description": descr,
        "url":url
    }
    response = sh.add_doc(coll_id, json, file_bytes, filename)
    if "detail" in response:
        await message.answer(f'Ошибка: {response.get("detail")}')
    else:
        await message.answer(f"Документ добавлен. Название: {name}, описание: {descr}, ссылка: {url}")
    await state.clear()

#удалить документ
@documents_router.callback_query(st.StateAndCallbackFilter("delete_doc", st.ViewCollections.view))
async def choose_doc_to_del(callback: CallbackQuery, state: FSMContext):
    user_id: int = callback.from_user.id
    data = await state.get_data()
    coll_id: int = data.get("id")
    await state.set_state(st.DeleteDoc.choose_doc)
    await state.update_data(coll_id=coll_id)
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
        await callback.message.edit_text('Выберите документ для удаления', reply_markup=keyboard)

#непосредственно удаление
@documents_router.callback_query(st.StateAndCallbackStartsWithFilter("select_document:",
                                                                     st.DeleteDoc.choose_doc))
async def delete_doc(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    coll_id: int = data.get("id", -1)
    user_id: int = callback.from_user.id
    doc_id: int = callback.data.split(":")[1]
    await callback.answer("")
    response = await sh.delete_doc(coll_id, doc_id, user_id)
    if response == "success":
        await callback.message.answer("Документ успешно удалён")
    else:
        await callback.message.answer(f"Ошибка: {response}")
    await state.clear()

