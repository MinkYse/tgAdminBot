from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import phonenumbers

from typing import List
import uuid
import re

from asgiref.sync import sync_to_async
import bot.Keyboards as kb
from bot.builders import profile, create_keyboard
from bot.states import Form
from bot.models import Seller, Category, Region, Hotel
from aiogram_media_group import media_group_handler

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


@sync_to_async
def create_user(message):
    Seller.objects.get_or_create(
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


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.who)
    await message.answer("Здравствуйтe, вы готовы?", reply_markup=kb.da)
    await create_user(message)

@router.callback_query(Form.who)
async def who(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.answer("Кто ты воин?", reply_markup=kb.menu)
    await state.set_state(Form.correct_who)


@router.callback_query(Form.correct_who)
async def cor1(clbk: CallbackQuery, state: FSMContext):
    c = clbk.data
    await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.update_data(who=clbk.data)
    await state.set_state(Form.check_who)

@router.callback_query(Form.check_who)
async def prov1(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_position)
        await clbk.message.answer("Введите, что вы хотите добавить?", reply_markup=kb.wh_bus)
    elif clbk.data == "back":
        await clbk.message.answer("Кто ты воин?", reply_markup=kb.menu)
        await state.set_state(Form.correct_who)

'''
@router.callback_query(Form.position)
async def Bus(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(who=clbk.data)
    await state.set_state(Form.type_position)
    await clbk.message.answer("Введите, что вы хотите добавить?", reply_markup=kb.wh_bus)
'''


@router.callback_query(Form.correct_position)
async def cor2(clbk: CallbackQuery, state: FSMContext):
    c = clbk.data
    await state.update_data(position=clbk.data)
    if c == "Hotel":
        await state.set_state(Form.check_position_hotel)
        await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    elif c == "Service":
        await state.set_state(Form.check_position_service)
        await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)

@router.callback_query(Form.check_position_service)
async def prov2(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.update_data(username=clbk.from_user.username)
        await state.set_state(Form.correct_type_position_service)
        list_categories = await get_categories('Услуги')
        await clbk.message.answer("Выберите тип услуги", reply_markup=create_keyboard(list_categories))
    elif clbk.data == "back":
        await clbk.message.answer("Введите, что вы хотите добавить?", reply_markup=kb.wh_bus)
        await state.set_state(Form.correct_position)

@router.callback_query(Form.check_position_hotel)
async def prov2(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.update_data(username=clbk.from_user.username)
        await state.set_state(Form.correct_type_position)
        list_categories = await get_categories('Отели')
        await clbk.message.answer("Выберите тип размещения", reply_markup=create_keyboard(list_categories))
    elif clbk.data == "back":
        await clbk.message.answer("Введите, что вы хотите добавить?", reply_markup=kb.wh_bus)
        await state.set_state(Form.correct_position)


'''
@router.callback_query(F.data == "Hotel")
async def position(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(username=clbk.from_user.username)
    await state.update_data(position=clbk.data)
    await state.set_state(Form.name)
    list_categories = await get_categories('Отели')
    await clbk.message.answer("Выберите тип размещения", reply_markup=create_keyboard(list_categories))
'''
@router.callback_query(Form.correct_type_position_service)
async def cor3(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    c = clbk.data
    await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(Form.check_type_position_service)

@router.callback_query(Form.check_type_position_service)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_name)
        await clbk.message.answer("Введите название фирмы")
    elif clbk.data == "back":
        list_categories = await get_categories('Услуги')
        await clbk.message.answer("Выберите тип услуги", reply_markup=create_keyboard(list_categories))
        await state.set_state(Form.correct_type_position_service)

@router.callback_query(Form.correct_type_position)
async def cor3(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    c = clbk.data
    await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(Form.check_type_position)

@router.callback_query(Form.check_type_position)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_name)
        await clbk.message.answer("Введите название отеля")
    elif clbk.data == "back":
        list_categories = await get_categories('Отели')
        await clbk.message.answer("Выберите тип размещения", reply_markup=create_keyboard(list_categories))
        await state.set_state(Form.correct_type_position)
'''        
@router.callback_query(Form.name)
async def name(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    await state.set_state(Form.photo)
    await clbk.message.answer("Введите название отеля")
'''

@router.message(Form.correct_name)
async def cor4(message: Message, state: FSMContext):
    c = message.text
    await state.update_data(name=c)
    await message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(Form.check_name)

@router.callback_query(Form.check_name)
async def prov4(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.photo_get)
        await clbk.message.answer("Отправьте 1-3 фото")
    elif clbk.data == "back":
        await clbk.message.answer("Введите название отеля")
        await state.set_state(Form.correct_name)

@router.message(F.media_group_id, Form.photo_get)
@media_group_handler
async def photo(messages: List[types.Message], state: FSMContext):
    list_photo = []
    for m in messages:
        await m.bot.download(file=m.photo[-1].file_id, destination=f'media/{str(uuid.uuid4().hex)}.jpg')
        list_photo.append(f'media/{str(uuid.uuid4().hex)}.jpg')
    await state.update_data(photos=list_photo)
    await messages[0].answer("Фото приняты, вы в них уверены?", reply_markup=kb.check)
    await state.set_state(Form.check_photo)

@router.message(Form.photo_get)
async def photo(message: Message, state: FSMContext):
    list_photo = []
    await message.bot.download(file=message.photo[-1].file_id, destination=f'media/{str(uuid.uuid4().hex)}.jpg')
    list_photo.append(f'media/{str(uuid.uuid4().hex)}.jpg')
    await state.update_data(photos=list_photo)
    await message.answer("Фото приняты, вы в них уверены?", reply_markup=kb.check)
    await state.set_state(Form.check_photo)


@router.callback_query(Form.check_photo)
async def prov5 (clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_number)
        await clbk.message.answer("Введите номер телефона")
    elif clbk.data == "back":
        await clbk.message.answer("Отправьте 1-3 фото")
        await state.set_state(Form.photo_get)

@router.message(Form.correct_number)
async def cor6(message: Message, state: FSMContext):
    c = message.text
    await state.update_data(phone=c)
    await message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(Form.check_number)

@router.callback_query(Form.check_number)
async def prov6(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await clbk.message.answer("Введите описание")
        await state.set_state(Form.correct_description)
    elif clbk.data == "back":
        await clbk.message.answer("Введите номер телефона")
        await state.set_state(Form.correct_number)


'''
@router.message(Form.photo)
async def type_position(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отправьте 1-3 фото")
    await state.set_state(Form.photo_get)
'''

'''
@router.message(Form.phone)
async def phone(message: Message, state: FSMContext):
    phone_number = phonenumbers.parse(message.text)
    if phonenumbers.is_possible_number(phone_number):
        await state.update_data(phone=message.text)
        await state.set_state(Form.description)
        await message.answer("Введите описание")
    else:
        await message.answer("Введите правильный контактный номер")
'''
@router.message(Form.correct_description)
async def cor7 (message: Message, state: FSMContext):
    c = message.text
    await state.update_data(description=c)
    await message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(Form.check_description)

@router.callback_query(Form.check_description)
async def prov7 (clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(Form.correct_min_money)
        await clbk.message.answer("Введите минимальную цену")
    elif clbk.data == "back":
        await clbk.message.answer("Введите описание")
        await state.set_state(Form.correct_description)

'''        
@router.message(Form.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Form.min_money)
    await message.answer("Введите минимальную цену")
'''

@router.message(Form.correct_min_money)
async def cor8(message: Message, state: FSMContext):
    if message.text.isdigit():
        c = message.text
        await state.update_data(min_money=c)
        await state.set_state(Form.check_min_money)
        await message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильную минимальную цену")

@router.callback_query(Form.check_min_money)
async def prov8(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await clbk.message.answer("Введите максимальную цену")
        await state.set_state(Form.correct_max_money)
    elif clbk.data == "back":
        await clbk.message.answer("Введите минимальную цену")
        await state.set_state(Form.correct_min_money)

'''   
@router.message(Form.min_money)
async def min_money(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(min_money=message.text)
        await state.set_state(Form.max_money)
        await message.answer("Введите максимальную цену")
    else:
        await message.answer("Введите правильную минимальную цену")
'''

@router.message(Form.correct_max_money)
async def cor9(message: Message, state: FSMContext):
    if message.text.isdigit():
        c = message.text
        await state.update_data(max_money=c)
        await state.set_state(Form.check_max_money)
        await message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильную максимальную цену")

@router.callback_query(Form.check_max_money)
async def prov9(clbk: CallbackQuery, state: CallbackQuery):
    if clbk.data == "continue":
        await clbk.message.answer("Введите адрес в формате 'Город, улица, дом'")
        await state.set_state(Form.correct_address)
    elif clbk.data == "back":
        await clbk.message.answer("Введите максимальную цену")
        await state.set_state(Form.correct_max_money)


'''       
@router.message(Form.max_money)
async def max_money(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(max_money=message.text)
        await state.set_state(Form.adres)
        await message.answer("Введите адрес в формате 'Город, улица, дом'")
    else:
        await message.answer("Введите правильную максимальную цену")
'''

@router.message(Form.correct_address)
async def cor10(message: Message, state: FSMContext):
    c = message.text
    if check_address(c):
        await state.update_data(geo_position=c)
        await message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
        await state.set_state(Form.check_address)
    else:
        await message.answer("Введите правильно адрес")

@router.callback_query(Form.check_address)
async def prov10(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        all_regions = await get_regions()
        await clbk.message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
        await state.set_state(Form.correct_get_district)
    elif clbk.data == "back":
        await clbk.message.answer("Введите адрес в формате 'Город, улица, дом'")
        await state.set_state(Form.correct_address)

@router.callback_query(Form.correct_get_district)
async def cor11(clbk: CallbackQuery, state: FSMContext):
    c = clbk.data
    await state.update_data(get_distriction=c)
    await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)
    await state.set_state(Form.check_get_district)

@router.callback_query(Form.check_get_district)
async def prov11(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        data = await state.get_data()
        await state.clear()
        await clbk.message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию")

        #hotel = Hotel()
        #await create_product(hotel, data)
        formatted_text = []
        [
            formatted_text.append(f"{key}: {value}")
            for key, value in data.items()
        ]
        await clbk.message.answer(f"{formatted_text}")
    elif clbk.data == "back":
        all_regions = await get_regions()
        await clbk.message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
        await state.set_state(Form.correct_get_district)


'''
@router.message(Form.adres)
async def geo_position(message: Message, state: FSMContext):
    if check_address(message.text):
        await state.update_data(geo_position=message.text)
        await state.set_state(Form.get_district)
        all_regions = await get_regions()
        await message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
    else:
        await message.answer('Исправьте адрес')
'''
'''
@router.callback_query(Form.get_district)
async def get_distriction(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(get_distriction=clbk.data)
    data = await state.get_data()
    await state.clear()
    await clbk.message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию")

    hotel = Hotel()
    await create_product(hotel, data)
    formatted_text = []
    [
        formatted_text.append(f"{key}: {value}")
        for key, value in data.items()
    ]
    await clbk.message.answer(f"{formatted_text}")
'''
'''
@router.callback_query(F.data == "Service")
async def position(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(username=clbk.from_user.username)
    await state.update_data(position=clbk.data)
    await state.set_state(Form.name_service)
    list_categories = await get_categories('Услуги')
    await clbk.message.answer("Выберите тип услуги", reply_markup=create_keyboard(list_categories))

@router.callback_query(Form.name_service)
async def name(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=clbk.data)
    await state.set_state(Form.photo)
    await clbk.message.answer("Введите название фирмы")
'''

'''
@router.message(Form.photo)
async def type_position(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отправьте 1-3 фото")
    await state.set_state(Form.photo_get)

@router.message(Form.photo_get)
@media_group_handler
async def photo(messages: List[types.Message], state: FSMContext):
    list_photo = []
    for m in messages:
        await m.bot.download(file=m.photo[-1].file_id, destination=f'media/{str(uuid.uuid4().hex)}.jpg')
        list_photo.append(f'media/{str(uuid.uuid4().hex)}.jpg')
    await state.update_data(photos=list_photo)
    await messages[0].answer('Введите номер телефона')
    await state.set_state(Form.phone)

@router.message(Form.photo_get)
async def photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(Form.phone)
    await message.answer("Введите свой контактный номер")

@router.message(Form.phone)
async def phone(message: Message, state: FSMContext):
    phone_number = phonenumbers.parse(message.text)
    if phonenumbers.is_possible_number(phone_number):
        await state.update_data(phone=message.text)
        await state.set_state(Form.description)
        await message.answer("Введите описание")
    else:
        await message.answer("Введите правильный контактный номер")

@router.message(Form.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Form.min_money)
    await message.answer("Введите минимальную цену")

@router.message(Form.min_money)
async def min_money(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(min_money=message.text)
        await state.set_state(Form.max_money)
        await message.answer("Введите максимальную цену")
    else:
        await message.answer("Введите правильную минимальную цену")

@router.message(Form.max_money)
async def max_money(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(max_money=message.text)
        await state.set_state(Form.adres)
        await message.answer("Введите адрес в формате 'Город, улица, дом'")
    else:
        await message.answer("Введите правильную максимальную цену")


@router.message(Form.adres)
async def geo_position(message: Message, state: FSMContext):
    if check_address(message.text):
        await state.update_data(geo_position=message.text)
        await state.set_state(Form.get_district)
        all_regions = await get_regions()
        await message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
    else:
        await message.answer('Исправьте адрес')


@router.callback_query(Form.get_district)
async def get_distriction(clbk: CallbackQuery, state: FSMContext):
    await state.update_data(get_distriction=clbk.data)
    data = await state.get_data()
    await state.clear()
    await clbk.message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию")

    #hotel = Hotel()
    #await create_product(hotel, data)
    formatted_text = []
    [
        formatted_text.append(f"{key}: {value}")
        for key, value in data.items()
    ]
    await clbk.message.answer(f"{formatted_text}")
'''