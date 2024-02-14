from aiogram import Router, F, types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models import Hotel, Service

from asgiref.sync import sync_to_async


@sync_to_async
def change_hotel_status(product_id):
    hotel = Hotel.objects.get(id=product_id)
    hotel.is_active = True
    hotel.save()


@sync_to_async
def change_service_status(product_id):
    service = Service.objects.get(id=product_id)
    service.is_active = True
    service.save()


@sync_to_async
def delete_hotel(product_id):
    hotel = Hotel.objects.get(id=product_id)
    hotel.delete()


@sync_to_async
def delete_service(product_id):
    service = Service.objects.get(id=product_id)
    service.delete()


@sync_to_async
def get_user_by_id(user_id):
    tg_id = Hotel.objects.get(id=user_id).owner.tg_id
    return tg_id


@sync_to_async
def get_user_service_by_id(user_id):
    tg_id = Service.objects.get(id=user_id).owner.tg_id
    return tg_id


admin_router = Router()


@admin_router.callback_query(F.data.startswith('agree'))
async def admin_agree(call: types.callback_query, bot: Bot):
    data = call.data.split('-')
    user_id = data[1]
    if data[2] == 'Размещение':
        tg_id = await get_user_by_id(user_id)
        await change_hotel_status(user_id)
    else:
        tg_id = await get_user_service_by_id(user_id)
        await change_service_status(user_id)
    await bot.send_message(chat_id=tg_id, text='Поздравляем! Ваша заявка прошла модерацию')


@admin_router.callback_query(F.data.startswith('disagree'))
async def admin_agree(call: types.callback_query, bot: Bot):
    data = call.data.split('-')
    user_id = data[1]
    if data[2] == 'Размещение':
        tg_id = await get_user_by_id(user_id)
        await delete_hotel(user_id)
    else:
        tg_id = await get_user_service_by_id(user_id)
        await delete_service(user_id)
    await bot.send_message(chat_id=tg_id, text='<b>К сожалению ваша заявка не прошла модерацию</b>\n'
                                               'Попробуйте сделать вашу заявку более подробной')


