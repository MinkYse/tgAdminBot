from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import re
import bot.keyboards_client as kb
from bot.builders import profile
from bot.states_client import ClientForm
from bot.states import Form
from bot.builders import create_keyboard
from asgiref.sync import sync_to_async
from bot.models import Category, Region, Service, Hotel

client_router = Router()

def is_date(text):
    date_patterns = [
        r'\d{1,2}.\d{1,2}.\d{4}',  # формат 11.11.2022
        r'\d{1,2} \w+ \d{4}'  # формат 10 февраля 2022
    ]
    for pattern in date_patterns:
        if re.search(pattern, text):
            return True
    return False

@sync_to_async
def get_product_by_id(product, product_id):
    result = product.objects.get(pk=product_id)
    return result


@sync_to_async
def get_product_by_region(region):
    products = Hotel.objects.filter(region__name=region)
    return [product.id for product in products]


@sync_to_async
def get_categories(type):
    all_categories = Category.objects.filter(type=type)
    return [category.name for category in all_categories]


@sync_to_async
def get_regions():
    all_regions = Region.objects.all()
    return [region.name for region in all_regions]

@client_router.callback_query(ClientForm.check_who)
async def prov1(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_position)
        await clbk.message.answer("Выберите, что вы хотите?", reply_markup=kb.wh_bus)
    elif clbk.data == "back":
        await clbk.message.answer("Кто ты воин?", reply_markup=kb.menu)
        await state.set_state(Form.correct_who)

@client_router.callback_query(ClientForm.correct_position)
async def cor2(clbk: CallbackQuery, state: FSMContext):
    c = clbk.data
    await state.update_data(position=clbk.data)
    if c == "Размещение":
        await state.set_state(ClientForm.check_position_hotel)
        await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    elif c == "Услуга":
        await state.set_state(ClientForm.check_position_service)
        await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)

@client_router.callback_query(ClientForm.check_position_service)
async def prov2(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.update_data(username=clbk.from_user.username)
        await state.set_state(ClientForm.correct_type_position_service)
        list_categories = await get_categories('Услуги')
        await clbk.message.answer("Выберите тип услуги", reply_markup=create_keyboard(list_categories))
    elif clbk.data == "back":
        await clbk.message.answer("Выберите, что вы хотите?", reply_markup=kb.wh_bus)
        await state.set_state(ClientForm.correct_position)

@client_router.callback_query(ClientForm.check_position_hotel)
async def prov2(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.update_data(username=clbk.from_user.username)
        await state.set_state(ClientForm.correct_type_position_hotel)
        list_categories = await get_categories('Отели')
        await clbk.message.answer("Выберите тип размещения", reply_markup=create_keyboard(list_categories))
    elif clbk.data == "back":
        await clbk.message.answer("Выберите, что вы хотите?", reply_markup=kb.wh_bus)
        await state.set_state(ClientForm.correct_position)

@client_router.callback_query(ClientForm.correct_type_position_service)
async def cor3(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    c = clbk.data
    await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(ClientForm.check_type_position_service)

@client_router.callback_query(ClientForm.correct_type_position_hotel)
async def cor3(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    c = clbk.data
    await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(ClientForm.check_type_position_hotel)

@client_router.callback_query(ClientForm.check_type_position_service)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_date_service)
        await clbk.message.answer("Введите желаемую дату")
    elif clbk.data == "back":
        list_categories = await get_categories('Услуги')
        await clbk.message.answer("Выберите тип услуги", reply_markup=create_keyboard(list_categories))
        await state.set_state(ClientForm.correct_type_position_service)

@client_router.callback_query(ClientForm.check_type_position_hotel)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_data)
        await clbk.message.answer("Введите дату заселения")
    elif clbk.data == "back":
        list_categories = await get_categories('Отели')
        await clbk.message.answer("Выберите тип размещения", reply_markup=create_keyboard(list_categories))
        await state.set_state(ClientForm.correct_type_position_hotel)

@client_router.message(ClientForm.correct_data)
async def cor4(message: Message, state: FSMContext):
    if is_date(message.text):
        await state.update_data(data_first=message.text)
        await state.set_state(ClientForm.check_data)
        await message.answer(f"Вы уверенны в своем выборе: {message.text}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильную дату заселения")

@client_router.message(ClientForm.correct_data_service)
async def cor4(message: Message, state: FSMContext):
    if is_date(message.text):
        await state.update_data(data_first=message.text)
        await state.set_state(ClientForm.check_data_service)
        await message.answer(f"Вы уверенны в своем выборе: {message.text}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильную дату")

@client_router.callback_query(ClientForm.check_data)
async def prov5(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_data_second)
        await clbk.message.answer("Введите дату выселения")
    elif clbk.data == "back":
        await clbk.message.answer("Введите дату заселения")
        await state.set_state(ClientForm.correct_data)

@client_router.message(ClientForm.correct_data_second)
async def cor5(message: Message, state: FSMContext):
    if is_date(message.text):
        await state.update_data(data_second=message.text)
        await state.set_state(ClientForm.check_data_second)
        await message.answer(f"Вы уверенны в своем выборе: {message.text}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильную дату")

@client_router.callback_query(ClientForm.check_data_second)
async def prov6(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_district)
        all_regions = await get_regions()
        await clbk.message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
    elif clbk.data == "back":
        await clbk.message.answer("Введите дату выселения")
        await state.set_state(ClientForm.correct_data_second)

@client_router.callback_query(ClientForm.check_data_service)
async def prov6(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_district)
        all_regions = await get_regions()
        await clbk.message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
    elif clbk.data == "back":
        await clbk.message.answer("Введите желаемую дату")
        await state.set_state(ClientForm.correct_data_service)

@client_router.callback_query(ClientForm.correct_district)
async def cor7(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(district=clbk.data)
    await state.set_state(ClientForm.check_district)
    await clbk.message.answer(f"Вы уверенны в своем выборе: {clbk.data}", reply_markup=kb.check)

@client_router.callback_query(ClientForm.check_district)
async def prov7(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await clbk.message.answer("Мы отправили вашу заявку")
        data = await state.get_data()
        id = await get_product_by_region(data["district"])
        print(id)
    elif clbk.data == "back":
        all_regions = await get_regions()
        await clbk.message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
        await state.set_state(ClientForm.correct_district)


