from aiogram.fsm.state import StatesGroup, State


class ClientForm(StatesGroup):
    position = State()
    check_who = State()
    correct_position = State()
    check_position_hotel = State()
    check_position_service = State()
    correct_type_position_service = State()
    correct_type_position_hotel = State()
    check_type_position_service = State()
    check_type_position_hotel = State()
    type_position = State()
    correct_data = State()
    correct_data_second = State()
    correct_data_service = State()
    check_data = State()
    check_data_service = State()
    check_data_second = State()
    correct_district = State()
    check_district = State()
    choice = State()
