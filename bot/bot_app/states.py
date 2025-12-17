from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

class AddNewcollection(StatesGroup):
    coll_name: State = State()
    coll_descr: State = State()

class DeleteCollection(StatesGroup):
    coll_name: State = State()

#ввод rag-запроса
class InputQuery(StatesGroup):
    choose_coll: State = State()
    input_query: State = State()

#ввод запроса на поиск документа
class DocSearch(StatesGroup):
    choose_coll: State = State()
    choose_number_of_sources: State = State()
    input_query: State = State()

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
