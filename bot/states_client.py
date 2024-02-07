from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    position = State()
    type_position = State()
    first_date = State()
    last_date = State()
    choice = State()
