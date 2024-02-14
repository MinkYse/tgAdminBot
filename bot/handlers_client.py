from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import re
import bot.keyboards_client as kb
from bot.builders import profile
from bot.states_client import ClientForm
from bot.states import Form
from bot.builders import create_keyboard, client_keyboard, confirm_keyboard
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
def get_hotel_by_id(product_id):
    result = Hotel.objects.get(pk=product_id)
    data = {
        'name': result.name,
        'photos': result.image,
        'description': result.description,
        'phone': result.phone_number,
        'owner': result.owner.tg_id,
        'address': result.address
    }
    return data


@sync_to_async
def get_service_by_id(product_id):
    result = Service.objects.get(pk=product_id)
    data = {
        'name': result.name,
        'photos': result.image,
        'description': result.description,
        'phone': result.phone_number,
        'owner': result.owner.tg_id,
        'address': result.address
    }
    return data


@sync_to_async
def get_hotel_by_region_and_type(region, category):
    products = Hotel.objects.filter(region__name=region, category__name=category, is_active=True)
    product_list = []
    for product in products:
        data = {
            'owner_id': product.owner.tg_id,
            'product_id': product.id,
            'product_name': product.name,
            'pruduct_address': product.address
        }
        product_list.append(data)
    return product_list


@sync_to_async
def get_service_by_region_and_type(region, category):
    products = Service.objects.filter(region__name=region, category__name=category, is_active=True)
    product_list = []
    for product in products:
        data = {
            'owner_id': product.owner.tg_id,
            'product_id': product.id,
            'product_name': product.name
        }
        product_list.append(data)
    return product_list


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
        await clbk.message.answer("Выберите свою роль", reply_markup=kb.menu)
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
        await state.set_state(ClientForm.correct_count)
        await clbk.message.answer("Введите количество людей")
    elif clbk.data == "back":
        list_categories = await get_categories('Услуги')
        await clbk.message.answer("Выберите тип услуги", reply_markup=create_keyboard(list_categories))
        await state.set_state(ClientForm.correct_type_position_service)

@client_router.callback_query(ClientForm.check_type_position_hotel)
async def prov3(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_count)
        await clbk.message.answer("Введите количество человек")
    elif clbk.data == "back":
        list_categories = await get_categories('Отели')
        await clbk.message.answer("Выберите тип размещения", reply_markup=create_keyboard(list_categories))
        await state.set_state(ClientForm.correct_type_position_hotel)

@client_router.message(ClientForm.correct_count_service)
async def cor_count_service(message: Message, state:FSMContext):
    if message.text.isdigit():
        await state.update_data(count=message.text)
        await state.set_state(ClientForm.check_count_service)
        await message.answer(f"Вы уверенны в своем выборе: {message.text}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильное количество людей")
@client_router.message(ClientForm.correct_count)
async def cor_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(count=message.text)
        await state.set_state(ClientForm.check_count)
        await message.answer(f"Вы уверенны в своем выборе: {message.text}", reply_markup=kb.check)
    else:
        await message.answer("Введите правильное количество людей")

@client_router.callback_query(ClientForm.check_count_service)
async def check_count_service(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_data_service)
        await clbk.message.answer("Введите желаемую дату")
    elif clbk.data == "back":
        await clbk.message.answer("Введите количество человек")
        await state.set_state(ClientForm.correct_count_service)

@client_router.callback_query(ClientForm.check_count)
async def check_count(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_data)
        await clbk.message.answer("Введите дату заселения")
    elif clbk.data == "back":
        await clbk.message.answer("Введите количество человек")
        await state.set_state(ClientForm.correct_count)



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
async def prov7(clbk: CallbackQuery, state: FSMContext, bot: Bot):
    if clbk.data == "continue":
        await clbk.message.answer("Мы отправили вашу заявку")
        data = await state.get_data()
        await state.clear()
        if data['position'] == 'Размещение':
            products = await get_hotel_by_region_and_type(data["district"], data['type_position'])
            for product in products:
                await bot.send_message(
                    chat_id=product['owner_id'],
                    text=f'<b>Пришла заявка от пользователя, по параметрам подходящая вашему отелю {product["product_name"]}</b>\n\n'
                         f'Колличество гостей: {data["count"]}\n'
                         f'Даты проживаня: с {data["data_first"]} по {data["data_second"]}\n',
                    reply_markup=client_keyboard(user_id=clbk.from_user.id,
                                                 product_id=product['product_id'],
                                                 position=data['position'])
                )
        else:
            products = await get_service_by_region_and_type(data['district'], data['type_position'])

            for product in products:
                await bot.send_message(
                    chat_id=product['owner_id'],
                    text=f'<b>Пришла заявка от пользователя, по параметрам подходящая вашему сервису {product["product_name"]}</b>\n\n'
                    f'Колличество желающих: {data["count"]}\n'
                    f'Желаемая дата: {data["data_first"]}',
                    reply_markup=client_keyboard(user_id=clbk.from_user.id,
                                                 product_id=product['product_id'],
                                                 position=data['position'])
                )
        print(clbk.from_user.id)
    elif clbk.data == "back":
        all_regions = await get_regions()
        await clbk.message.answer("Выберите район", reply_markup=create_keyboard(all_regions))
        await state.set_state(ClientForm.correct_district)


@client_router.callback_query(F.data.startswith('offer'))
async def admin_agree(call: CallbackQuery, bot: Bot):
    data = call.data.split('-')
    print(data)
    print()
    if data[3] == 'Размещение':
        product = await get_hotel_by_id(data[2])
    else:
        product = await get_service_by_id(data[2])

    await call.message.delete_reply_markup()
    media = [InputMediaPhoto(types='photo',
                                   media=FSInputFile(fr'media/{ph}')) for ph in product['photos']]
    await bot.send_media_group(chat_id=data[1], media=media)
    await bot.send_message(chat_id=data[1], text=f'<b>{product["name"]} одобряет вашу заявку</b>\n\n'
                           f'Описание: {product["description"]}\n'
                           f'Номер телефона: {product["phone"]}'
                           f'Адрес: https://yandex.ru/maps/?text={product["address"]}',
                           reply_markup=confirm_keyboard(product['owner'], call.from_user.username, product['name']))


@client_router.callback_query(F.data.startswith('confirm'))
async def confirm_client(call: CallbackQuery, bot: Bot):
    data = call.data.split('-')
    print('Работает')
    print(data)
    await call.message.delete_reply_markup()
    await bot.send_message(chat_id=data[1], text=f'<b>Пользователь {call.from_user.username} подтвердил своё бронирование вашего отеля {data[3]}</b>')
