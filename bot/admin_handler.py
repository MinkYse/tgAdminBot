from aiogram import Router, F, types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models import Hotel

from asgiref.sync import sync_to_async


@sync_to_async
def get_user_by_id(user_id):
    tg_id = Hotel.objects.filter(id=user_id)[0].owner.tg_id
    return tg_id


admin_router = Router()


@admin_router.callback_query(F.data.startswith('agree'))
async def admin_agree(call: types.callback_query, bot: Bot):
    user_id = call.data.split('-')[1]
    tg_id = await get_user_by_id(user_id)
    await bot.send_message(chat_id=tg_id, text='Поздравляем! Ваша заявка прошла модерацию')


@admin_router.callback_query(F.data.startswith('disagree'))
async def admin_agree(call: types.callback_query, bot: Bot):
    user_id = call.data.split('-')[1]
    tg_id = await get_user_by_id(user_id)
    await bot.send_message(chat_id=tg_id, text='К сожалению ваша заявка не прошла модерацию')