from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)
from constants import *

wh_bus = [
    [
        InlineKeyboardButton(text=f"{TYPE_CLIENT_ONE}", callback_data="Размещение"),
        InlineKeyboardButton(text=f"{TYPE_CLIENT_TWO}", callback_data="Услуга")
    ]
]
wh_bus = InlineKeyboardMarkup(inline_keyboard=wh_bus)

check = [
    [
        InlineKeyboardButton(text=f"{CONTINUE}", callback_data="continue"),
        InlineKeyboardButton(text=f"{BACK}", callback_data="back")
    ]
]
check = InlineKeyboardMarkup(inline_keyboard=check)


