from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import bot.keyboards_client as kb
from bot.builders import profile
from bot.states_client import ClientForm
from bot.states import Form
from bot.builders import create_keyboard

client_router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.position)
    await message.answer("Здравствуйте, выберите, что ищите", reply_markup=kb.main_kb)


@router.message(F.text == "Услуга")
async def position(message: Message, state: FSMContext):
    msg = message.text.lower()
    if msg == "размещение":
        await state.update_data(position=msg)
        await state.set_state(Form.type_position)
        await message.answer("Выберите тип размещения", reply_markup=kb.hotel_kb)

        @router.message(Form.type_position)
        async def type_position(message: Message, state: FSMContext):
            await state.update_data(type_position=message.text)
            await state.set_state(Form.first_date)
            await message.answer("Введите дату заезда", reply_markup=kb.rmk)

        @router.message(Form.first_date)
        async def first_date(message: Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(first_date=message.text)
                await state.set_state(Form.last_date)
                await message.answer("Введите дату съезда")
            else:
                await message.answer("Введите правильную дату заезда")

        @router.message(Form.last_date)
        async def last_date(message: Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(last_date=message.text)
                await state.set_state(Form.choice)
                await message.answer("Вот что мы можем предложить)", reply_markup=profile(["Отель1", "Отель2", "Отель3", "Отель4", "Отель5"]))
            else:
                await message.answer("Введите правильную дату съезда")

        @router.message(Form.choice)
        async def choice(message: Message, state: FSMContext):
            await state.update_data(choice=message.text)
            data = await state.get_data()
            await state.clear()
            await message.answer("Спасибо, что выбрали нас!", reply_markup=kb.rmk)

            formatted_text = []
            [
                formatted_text.append(f"{key}: {value}")
                for key, value in data.items()
            ]
            await message.answer(f"{formatted_text}")

    elif msg == "услуга":
        await state.update_data(position=msg)
        await state.set_state(Form.type_position)
        await message.answer("Выберите тип услуги", reply_markup=kb.service_kb)

        @router.message(Form.type_position)
        async def type_position(message: Message, state: FSMContext):
            await state.update_data(type_position=message.text)
            await state.set_state(Form.first_date)
            await message.answer("Введите дату заезда", reply_markup=kb.rmk)

        @router.message(Form.first_date)
        async def first_date(message: Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(first_date=message.text)
                await state.set_state(Form.last_date)
                await message.answer("Введите дату съезда")
            else:
                await message.answer("Введите правильную дату заезда")

        @router.message(Form.last_date)
        async def last_date(message: Message, state: FSMContext):
            if message.text.isdigit():
                await state.update_data(last_date=message.text)
                await state.set_state(Form.choice)
                await message.answer("Вот что мы можем предложить)",
                                     reply_markup=profile(["Отель1", "Отель2", "Отель3", "Отель4", "Отель5"]))
            else:
                await message.answer("Введите правильную дату съезда")

        @router.message(Form.choice)
        async def choice(message: Message, state: FSMContext):
            await state.update_data(choice=message.text)
            data = await state.get_data()
            await state.clear()
            await message.answer("Спасибо, что выбрали нас!", reply_markup=kb.rmk)

            formatted_text = []
            [
                formatted_text.append(f"{key}: {value}")
                for key, value in data.items()
            ]
            await message.answer(f"{formatted_text}")


@client_router.callback_query(ClientForm.check_who)
async def prov1(clbk: CallbackQuery, state: FSMContext):
    if clbk.data == "continue":
        await state.set_state(ClientForm.correct_position)
        await clbk.message.answer("Что вас интересует?", reply_markup=kb.main_kb)
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
        await state.set_state(Form.check_position_service)
        await clbk.message.answer(f"Вы уверенны в своем выборе: {c}", reply_markup=kb.check)


@client_router.callback_query(ClientForm.check_position_service)
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