from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import phonenumbers

from typing import List
import uuid
import re

from asgiref.sync import sync_to_async
import bot.Keyboards as kb
from bot.builders import profile
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
    await state.set_state(Form.position)
    await message.answer("Здравствуйте, выберите, что будете добавлять", reply_markup=kb.main_kb)
    await create_user(message)


@router.message(F.text == "Услуга")
@router.message(F.text == "Размещение")
async def position(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "размещение":
        await state.update_data(username=message.from_user.username)
        await state.update_data(position=msg)
        await state.set_state(Form.type_position)
        list_categories = await get_categories('Отели')
        await message.answer("Выберите тип размещения", reply_markup=profile(list_categories))

        @router.message(Form.type_position)
        async def type_position(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(type_position=message.text)
                await state.set_state(Form.photo)
                await message.answer("Отправьте 1-3 фото", reply_markup=kb.cancel_kb)
            else:
                await state.set_state(Form.position)

        @router.message(Form.photo)
        @media_group_handler
        async def photo(messages: List[types.Message], state: FSMContext):
            counter = 1
            list_photo = []
            for m in messages:
                await m.bot.download(file=m.photo[-1].file_id, destination=f'media/{str(uuid.uuid4().hex)}.jpg')
                list_photo.append(f'media/{str(uuid.uuid4().hex)}.jpg')
            await state.update_data(photos=list_photo)
            await messages[0].answer('Введите номер телефона')
            await state.set_state(Form.phone)

        @router.message(Form.phone)
        async def phone(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                phone_number = phonenumbers.parse(message.text)
                if phonenumbers.is_possible_number(phone_number):
                    await state.update_data(phone=message.text)
                    await state.set_state(Form.description)
                    await message.answer("Введите описание", reply_markup=kb.cancel_kb)
                else:
                    await message.answer("Введите правильный контактный номер")
            else:
                await state.set_state(Form.photo)

        @router.message(Form.description)
        async def description(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(description=message.text)
                await state.set_state(Form.min_money)
                await message.answer("Введите минимальную цену", reply_markup=kb.cancel_kb)
            else:
                await state.set_state(Form.phone)

        @router.message(Form.min_money)
        async def min_money(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                if message.text.isdigit():
                    await state.update_data(min_money=message.text)
                    await state.set_state(Form.max_money)
                    await message.answer("Введите максимальную цену", reply_markup=kb.cancel_kb)
                else:
                    await message.answer("Введите правильную минимальную цену")
            else:
                await state.set_state(Form.description)

        @router.message(Form.max_money)
        async def max_money(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                if message.text.isdigit():
                    await state.update_data(max_money=message.text)
                    await state.set_state(Form.adres)
                    await message.answer("Введите адрес в формате 'Город, улица, дом'", reply_markup=kb.cancel_kb)
                else:
                    await message.answer("Введите правильную максимальную цену")
            else:
                await state.set_state(Form.min_money)

        @router.message(Form.adres)
        async def geo_position(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                if check_address(message.text):
                    await state.update_data(geo_position=message.text)
                    await state.set_state(Form.get_district)
                    all_regions = await get_regions()
                    await message.answer("Выберите район", reply_markup=profile(all_regions))
                else:
                    await message.answer('Исправьте адрес')
            else:
                await state.set_state(Form.max_money)

        @router.message(Form.get_district)
        async def get_distriction(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(get_distriction=message.text)
                data = await state.get_data()
                await state.clear()
                await message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию", reply_markup=kb.cancel_kb)

                hotel = Hotel()
                await create_product(hotel, data)
                formatted_text = []
                [
                    formatted_text.append(f"{key}: {value}")
                    for key, value in data.items()
                ]
                await message.answer(f"{formatted_text}")
            else:
                await state.set_state(Form.adres)

    elif msg == "услуга":
        await state.update_data(position=msg)
        await state.set_state(Form.type_position)
        await message.answer("Выберите тип услуги", reply_markup=kb.service_kb)

        @router.message(Form.type_position)
        async def type_position(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(type_position=message.text)
                await state.set_state(Form.photo)
                await message.answer("Отправьте 1-3 фото", reply_markup=kb.cancel_kb)
            else:
                await state.set_state(Form.position)

        @router.message(Form.photo)
        async def photo(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(photo=message.photo[-1].file_id)
                await state.set_state(Form.phone)
                await message.answer("Введите свой контактный номер", reply_markup=kb.cancel_kb)
            else:
                await state.set_state(Form.type_position)

        @router.message(Form.phone)
        async def phone(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                if message.text.isdigit():
                    await state.update_data(phone=message.text)
                    await state.set_state(Form.description)
                    await message.answer("Введите описание", reply_markup=kb.cancel_kb)
                else:
                    await message.answer("Введите правильный контактный номер")
            else:
                await state.set_state(Form.photo)

        @router.message(Form.description)
        async def description(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(description=message.text)
                await state.set_state(Form.min_money)
                await message.answer("Введите минимальную цену", reply_markup=kb.cancel_kb)
            else:
                await state.set_state(Form.phone)

        @router.message(Form.min_money)
        async def min_money(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                if message.text.isdigit():
                    await state.update_data(min_money=message.text)
                    await state.set_state(Form.max_money)
                    await message.answer("Введите максимальную цену", reply_markup=kb.cancel_kb)
                else:
                    await message.answer("Введите правильную минимальную цену")
            else:
                await state.set_state(Form.description)

        @router.message(Form.max_money)
        async def max_money(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                if message.text.isdigit():
                    await state.update_data(max_money=message.text)
                    await state.set_state(Form.adres)
                    await message.answer("Введите адрес в формате 'Город, улица, дом'", reply_markup=kb.cancel_kb)
                else:
                    await message.answer("Введите правильную максимальную цену")
            else:
                await state.set_state(Form.min_money)

        @router.message(Form.adres)
        async def geo_position(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(geo_position=message.text)
                await state.set_state(Form.get_district)
                await message.answer("Выберите район", reply_markup=profile(
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Отмена"]))
            else:
                await state.set_state(Form.max_money)

        @router.message(Form.get_district)
        async def get_distriction(message: Message, state: FSMContext):
            if message.text.lower() != "назад":
                await state.update_data(get_distriction=message.text)
                data = await state.get_data()
                await state.clear()
                await message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию", reply_markup=kb.cancel_kb)

                formatted_text = []
                [
                    formatted_text.append(f"{key}: {value}")
                    for key, value in data.items()
                ]
                await message.answer(f"{formatted_text}")
            else:
                await state.set_state(Form.adres)