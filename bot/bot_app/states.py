from aiogram.fsm.state import StatesGroup, State

class AddNewcollection(StatesGroup):
    coll_name: State = State()
    coll_descr: State = State()

class DeleteCollection(StatesGroup):
    coll_name: State = State()