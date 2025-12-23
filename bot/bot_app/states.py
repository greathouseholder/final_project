from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

#просмотр коллекций
class ViewCollections(StatesGroup):
    view = State()

#добавление коллекции
class AddNewcollection(StatesGroup):
    coll_name = State()
    coll_descr = State()
    is_public = State()

#изменение коллекции
class UpdateCollection(StatesGroup):
    coll_name = State()
    coll_desc = State()

#удаление коллекции
class DeleteCollection(StatesGroup):
    coll_name = State()

#ввод rag-запроса
class InputQuery(StatesGroup):
    choose_coll = State()
    input_query = State()

#ввод запроса на поиск документа
class DocSearch(StatesGroup):
    choose_coll = State()
    choose_number_of_sources = State()
    input_query = State()

#добавление документа
class AddDoc(StatesGroup):
    input_name = State()
    input_desc = State()
    input_url = State()
    send_file = State()

#изменение документа
class UpdateDocument(StatesGroup):
    input_name = State()
    input_desc = State()

#удаление документа
class DeleteDoc(StatesGroup):
    choose_doc = State()
    is_sure = State() #опционально потом сделаю
    
#фильтр, который проверяет одновременно префикс колбэка и state
class StateAndCallbackStartsWithFilter(BaseFilter):
    def __init__(self, prefix: str, required_state: State):
        self.prefix = prefix
        self.required_state = required_state
    
    async def __call__(
        self, 
        callback: CallbackQuery, 
        state: FSMContext
    ) -> bool:
        if not callback.data or not callback.data.startswith(self.prefix):
            return False

        current_state = await state.get_state()
        return current_state == self.required_state
    
#фильтр, который проверяет одновременно колбэк и state
class StateAndCallbackFilter(BaseFilter):
    def __init__(self, required_callback: str, required_state: State):
        self.required_callback = required_callback
        self.required_state = required_state
    
    async def __call__(
        self, 
        callback: CallbackQuery, 
        state: FSMContext
    ) -> bool:
        if not callback.data or not callback.data == self.required_callback:
            return False

        current_state = await state.get_state()
        return current_state == self.required_state
