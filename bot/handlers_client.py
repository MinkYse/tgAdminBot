from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import keyboards_client as kb
from builders import profile
from states_client import Form

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.position)
    await message.answer("Здравствуйте, выберите, что ищите", reply_markup=kb.main_kb)

@router.message(F.text == "Услуга")
@router.message(F.text == "Размещение")
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


