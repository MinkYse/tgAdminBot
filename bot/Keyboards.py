from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)
from constants import *

menu = [
    [
        KeyboardButton(text=f"{USER_CLIENT}", callback_data="Клиент"),
        KeyboardButton(text=f"{USER_BUSNESSMAN}", callback_data="Предприниматель")
    ]
]
menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)

wh_bus = [
    [
        InlineKeyboardButton(text=f"{TYPE_BUSINESSMAN_ONE}", callback_data="Размещение"),
        InlineKeyboardButton(text=f"{TYPE_BUSINESSMAN_TWO}", callback_data="Услуга")
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


client =[
    [
        KeyboardButton(text=f"{CREATE_NEW_ORDER}")
    ]
]
client = ReplyKeyboardMarkup(keyboard=client, resize_keyboard=True, one_time_keyboard=True)

bussiness = [
    [
        KeyboardButton(text=f"{CREATE_NEW_ADVETISEMENT}")
    ]
]
bussiness = ReplyKeyboardMarkup(keyboard=bussiness, resize_keyboard=True, one_time_keyboard=True)