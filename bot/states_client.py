from aiogram.fsm.state import StatesGroup, State


class ClientForm(StatesGroup):
    position = State()
    check_who = State()
    correct_position = State()
    type_position = State()
    first_date = State()
    last_date = State()
    choice = State()
