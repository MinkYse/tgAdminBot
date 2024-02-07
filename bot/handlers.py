from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import Keyboards as kb
from builders import profile
from states import Form

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.position)
    await message.answer("Здравствуйте, выберите, что будете добавлять", reply_markup=kb.main_kb)


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
            await state.set_state(Form.photo)
            await message.answer("Отправьте 1-3 фото", reply_markup=kb.rmk)

        @router.message(Form.photo)
        async def photo(message: Message, state: FSMContext):
            await state.update_data(photo=message.photo[-1].file_id)
            await state.set_state(Form.phone)
            await message.answer("Введите свой контактный номер")

        @router.message(Form.phone)
        async def phone(message: Message, state: FSMContext):
            if message.text.isdigit():
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
                await state.set_state(Form.geo_position)
                await message.answer("Введите ссылку на геопозицию")
            else:
                await message.answer("Введите правильную максимальную цену")

        @router.message(Form.geo_position)
        async def geo_position(message: Message, state: FSMContext):
            await state.update_data(geo_position=message.text)
            await state.set_state(Form.get_district)
            await message.answer("Выберите район", reply_markup=profile(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))

        @router.message(Form.get_district)
        async def get_distriction(message: Message, state: FSMContext):
            await state.update_data(get_distriction=message.text)
            data = await state.get_data()
            await state.clear()
            await message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию", reply_markup=kb.rmk)

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
            await state.set_state(Form.photo)
            await message.answer("Отправьте 1-3 фото", reply_markup=kb.rmk)

        @router.message(Form.photo)
        async def photo(message: Message, state: FSMContext):
            await state.update_data(photo=message.photo[-1].file_id)
            await state.set_state(Form.phone)
            await message.answer("Введите свой контактный номер")

        @router.message(Form.phone)
        async def phone(message: Message, state: FSMContext):
            if message.text.isdigit():
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
                await state.set_state(Form.geo_position)
                await message.answer("Введите ссылку на геопозицию")
            else:
                await message.answer("Введите правильную максимальную цену")

        @router.message(Form.geo_position)
        async def geo_position(message: Message, state: FSMContext):
            await state.update_data(geo_position=message.text)
            await state.set_state(Form.get_district)
            await message.answer("Выберите район",
                                 reply_markup=profile(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))

        @router.message(Form.get_district)
        async def get_distriction(message: Message, state: FSMContext):
            await state.update_data(get_distriction=message.text)
            data = await state.get_data()
            await state.clear()
            await message.answer("Вы прошли опрос, ваша заявка отправлена на модерацию", reply_markup=kb.rmk)

            formatted_text = []
            [
                formatted_text.append(f"{key}: {value}")
                for key, value in data.items()
            ]
            await message.answer(f"{formatted_text}")

