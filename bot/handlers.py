from aiogram import Router, F, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from typing import List
import uuid
import re
import os
from asgiref.sync import sync_to_async

import bot.Keyboards as kb
from bot.builders import create_keyboard, create_admin_keyboard
from bot.states import Form
from bot.states_client import ClientForm
from bot.models import Seller, Category, Region, Hotel, Service, Client
from aiogram_media_group import media_group_handler
from constants import *

router = Router()


@sync_to_async
def create_product(product, data):
    product.name = data['name']
    product.phone_number = data['phone']
    product.image = data['photos']
    product.address = data['geo_position']
    product.min_price = data['min_money']
    product.max_price = data['max_money']
    product.description = data['description']
    product.category = Category.objects.get(name=data['type_position'])
    product.region = Region.objects.get(name=data['get_distriction'])
    product.owner = Seller.objects.get(username=data['username'])
    product.save()
    return product.id


@sync_to_async
def create_seller(message):
    Seller.objects.get_or_create(
        username=message.from_user.username,
        tg_id=message.from_user.id
    )


@sync_to_async
def create_client(message):
    Client.objects.get_or_create(
        username=message.from_user.username,
        tg_id=message.from_user.id
    )


@sync_to_async
def get_categories(type):
    all_categories = Category.objects.filter(type=type)
    return [category.name for category in all_categories]


@sync_to_async
def get_regions():
    all_regions = Region.objects.all()
    return [region.name for region in all_regions]


def check_address(address):
    pattern = r'^([а-яА-ЯёЁ ,.-]+),\s+([а-яА-ЯёЁ0-9 ,.-]+),\s+([0-9a-zA-Z]+)([а-яА-ЯёЁ]{0,1})$'
    match = re.match(pattern, address)
    if match:
        return True
    else:
        return False


def validate_phone_number(phone_number):
    # Удаление всех символов, кроме цифр
    phone_number = ''.join(c for c in phone_number if c.isdigit())
    print(phone_number)

    pattern = r'^[7-9]\d{10}$'

    # Проверка номера
    return bool(re.match(pattern, phone_number))


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(WELCOME, reply_markup=kb.menu)
    await state.set_state(Form.new_wait)


@router.message((F.text == "Клиент") | (F.text == "Предприниматель"))
async def get_info(message: Message, state: FSMContext):
    if message.text == "Клиент":
        await create_client(message)
        await message.answer(INFO, reply_markup=kb.client)
    else:
        await create_seller(message)
        await message.answer(INFO, reply_markup=kb.bussiness)


@router.message(F.text == CREATE_NEW_ADVETISEMENT)
async def prov1(message: Message, state: FSMContext):
    await state.set_state(Form.correct_position)
    await message.answer(CHOOSING_PRODUCT_TYPE, reply_markup=kb.wh_bus)


@router.callback_query(Form.correct_position)
async def cor2(clbk: CallbackQuery, state: FSMContext):
    c = clbk.data
    await state.update_data(position=clbk.data)
    if c == "Размещение":
        await state.set_state(Form.check_position_hotel)
        await clbk.message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    elif c == "Услуга":
        await state.set_state(Form.check_position_service)
        await clbk.message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)

@router.callback_query(Form.check_position_service)
async def prov2(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.update_data(username=clbk.from_user.username)
        await state.set_state(Form.correct_type_position_service)
        list_categories = await get_categories('Услуги')
        await clbk.message.answer(CHOOSING_SERVICE_CATEGORIES, reply_markup=create_keyboard(list_categories))
    elif clbk.data == "back":
        await clbk.message.answer(CHOOSING_PRODUCT_TYPE, reply_markup=kb.wh_bus)
        await state.set_state(Form.correct_position)

@router.callback_query(Form.check_position_hotel)
async def prov2(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.update_data(username=clbk.from_user.username)
        await state.set_state(Form.correct_type_position)
        list_categories = await get_categories('Отели')
        await clbk.message.answer(CHOOSING_HOTEL_CATEGORIES, reply_markup=create_keyboard(list_categories))
    elif clbk.data == "back":
        await clbk.message.answer(CHOOSING_PRODUCT_TYPE, reply_markup=kb.wh_bus)
        await state.set_state(Form.correct_position)


@router.callback_query(Form.correct_type_position_service)
async def cor3(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    c = clbk.data
    await clbk.message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    await state.set_state(Form.check_type_position_service)


@router.callback_query(Form.check_type_position_service)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_name)
        await clbk.message.answer(ENTER_SERVICE_NAME)
    elif clbk.data == "back":
        list_categories = await get_categories('Услуги')
        await clbk.message.answer(CHOOSING_SERVICE_CATEGORIES, reply_markup=create_keyboard(list_categories))
        await state.set_state(Form.correct_type_position_service)


@router.callback_query(Form.correct_type_position)
async def cor3(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    c = clbk.data
    await clbk.message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    await state.set_state(Form.check_type_position)


@router.callback_query(Form.check_type_position)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_name)
        await clbk.message.answer(ENTER_HOTEL_NAME)
    elif clbk.data == "back":
        list_categories = await get_categories('Отели')
        await clbk.message.answer(CHOOSING_HOTEL_CATEGORIES, reply_markup=create_keyboard(list_categories))
        await state.set_state(Form.correct_type_position)


@router.message(Form.correct_name)
async def cor4(message: Message, state: FSMContext):
    c = message.text
    await state.update_data(name=c)
    await message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    await state.set_state(Form.check_name)


@router.callback_query(Form.check_name)
async def prov4(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.photo_get)
        await clbk.message.answer(SEND_PHOTO)
    elif clbk.data == "back":
        await clbk.message.answer(ENTER_HOTEL_NAME)
        await state.set_state(Form.correct_name)


@router.message(F.media_group_id, Form.photo_get)
@media_group_handler
async def photo(messages: List[types.Message], state: FSMContext):
    list_photo = []
    for m in messages:
        photo_name = f'{str(uuid.uuid4().hex)}.jpg'
        await m.bot.download(file=m.photo[-1].file_id, destination=f'media/{photo_name}')
        list_photo.append(photo_name)
    await state.update_data(photos=list_photo)
    await messages[0].answer(GET_MORE_PHOTO, reply_markup=kb.check)
    await state.set_state(Form.check_photo)


@router.message(Form.photo_get)
async def photo(message: Message, state: FSMContext):
    photo_name = f'{str(uuid.uuid4().hex)}.jpg'
    list_photo = []
    await message.bot.download(file=message.photo[-1].file_id, destination=f'media/{photo_name}')
    list_photo.append(photo_name)
    await state.update_data(photos=list_photo)
    await message.answer(GET_ONE_PHOTO, reply_markup=kb.check)
    await state.set_state(Form.check_photo)


@router.callback_query(Form.check_photo)
async def prov5(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_number)
        await clbk.message.answer(SEND_NUMBER)
    elif clbk.data == "back":
        data = await state.get_data()
        for file in data['photos']:
            os.remove(f'media/{file}')
        await clbk.message.answer(SEND_PHOTO)
        await state.set_state(Form.photo_get)


@router.message(Form.correct_number)
async def cor6(message: Message, state: FSMContext):
    c = message.text
    if validate_phone_number(c):
        await state.update_data(phone=c)
        await message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
        await state.set_state(Form.check_number)
    else:
        await message.answer(CORRECT_NUMBER)


@router.callback_query(Form.check_number)
async def prov6(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await clbk.message.answer(SEND_DESCRIPTION)
        await state.set_state(Form.correct_description)
    elif clbk.data == "back":
        await clbk.message.answer(SEND_NUMBER)
        await state.set_state(Form.correct_number)


@router.message(Form.correct_description)
async def cor7(message: Message, state: FSMContext):
    c = message.text
    await state.update_data(description=c)
    await message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    await state.set_state(Form.check_description)


@router.callback_query(Form.check_description)
async def prov7(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_min_money)
        await clbk.message.answer(SEND_MIN_PRICE)
    elif clbk.data == "back":
        await clbk.message.answer(SEND_DESCRIPTION)
        await state.set_state(Form.correct_description)


@router.message(Form.correct_min_money)
async def cor8(message: Message, state: FSMContext):
    if message.text.isdigit():
        c = message.text
        await state.update_data(min_money=c)
        await state.set_state(Form.check_min_money)
        await message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    else:
        await message.answer(CORRECT_PRICE)


@router.callback_query(Form.check_min_money)
async def prov8(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await clbk.message.answer(SEND_MAX_PRICE)
        await state.set_state(Form.correct_max_money)
    elif clbk.data == "back":
        await clbk.message.answer(SEND_MIN_PRICE)
        await state.set_state(Form.correct_min_money)


@router.message(Form.correct_max_money)
async def cor9(message: Message, state: FSMContext):
    if message.text.isdigit():
        c = message.text
        await state.update_data(max_money=c)
        await state.set_state(Form.check_max_money)
        await message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    else:
        await message.answer(CORRECT_PRICE)



@router.callback_query(Form.check_max_money)
async def prov9(clbk: CallbackQuery, state: CallbackQuery):
    if clbk.data == "continue":
        await clbk.message.answer(SEND_ADDRESS)
        await state.set_state(Form.correct_address)
    elif clbk.data == "back":
        await clbk.message.answer(SEND_MAX_PRICE)
        await state.set_state(Form.correct_max_money)


@router.message(Form.correct_address)
async def cor10(message: Message, state: FSMContext):
    c = message.text
    address_list = [el.strip().capitalize() for el in c.split(',')]
    address_list[1] = f'ул. {address_list[1]}'
    c = ', '.join(address_list)
    if check_address(c):
        await state.update_data(geo_position=c)
        await message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
        await state.set_state(Form.check_address)
    else:
        await message.answer(CORRECT_ADDRESS)


@router.callback_query(Form.check_address)
async def prov10(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        all_regions = await get_regions()
        await clbk.message.answer(CHOICE_REGION, reply_markup=create_keyboard(all_regions))
        await state.set_state(Form.correct_get_district)
    elif clbk.data == "back":
        await clbk.message.answer(SEND_ADDRESS)
        await state.set_state(Form.correct_address)


@router.callback_query(Form.correct_get_district)
async def cor11(clbk: CallbackQuery, state: FSMContext):
    c = clbk.data
    await state.update_data(get_distriction=c)
    await clbk.message.answer(f"{CHECK_MESSAGE}: {c}?", reply_markup=kb.check)
    await state.set_state(Form.check_get_district)


@router.callback_query(Form.check_get_district)
async def prov11(clbk: CallbackQuery, state: FSMContext, bot: Bot):
    if clbk.data == "continue":
        data = await state.get_data()
        await state.clear()
        if data['position'] == 'Размещение':
            hotel = Hotel()
            product_id = await create_product(hotel, data)
        else:
            service = Service()
            product_id = await create_product(service, data)

        media = [types.InputMediaPhoto(types='photo', media=types.FSInputFile(fr'media/{ph}')) for ph in data['photos']]
        await bot.send_media_group(chat_id=ADMIN_CHAT_ID, media=media)
        await bot.send_message(chat_id=ADMIN_CHAT_ID,
                               text='<b>Созданно новое предложение!</b>\n\n'
                                    f'Номер заказа: {product_id}\n'
                                    f'Название {data["position"]}: {data["name"]}\n'
                                    f'Описание: {data["description"]}\n'
                                    f'Минимальная цена: {data["min_money"]}\n'
                                    f'Максимальная цена: {data["max_money"]}\n'
                                    f'Тип {data["position"]}: {data["type_position"]}\n'
                                    f'Адрес: {data["geo_position"]}\n'
                                    f'Номер телефона: {data["phone"]}\n'
                                    f'Район размещения: {data["get_distriction"]}',
                               reply_markup=create_admin_keyboard(product_id, data['position'])
                               )
        await clbk.message.answer(SUCCESS_MESSAGE, reply_markup=kb.bussiness)
    elif clbk.data == "back":
        all_regions = await get_regions()
        await clbk.message.answer(CHOICE_REGION, reply_markup=create_keyboard(all_regions))
        await state.set_state(Form.correct_get_district)

