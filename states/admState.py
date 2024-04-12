from aiogram.dispatcher.filters.state import StatesGroup, State

class addAdmSt(StatesGroup):
    admId = State()

class removeAdmSt(StatesGroup):
    admId = State()

class rek(StatesGroup):
    sendrek = State()

class wordSt(StatesGroup):
    addSt = State()

class removeSt(StatesGroup):
    remSt = State()