from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    position = State()
    type_position = State()
    photo = State()
    phone = State()
    description = State()
    min_money = State()
    max_money = State()
    adres = State()
    get_district = State()
    