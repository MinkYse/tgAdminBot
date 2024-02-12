from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)

wh_bus = [
    [
        InlineKeyboardButton(text="Размещение", callback_data="Размещение"),
        InlineKeyboardButton(text="Услуга", callback_data="Услуга")
    ]
]
wh_bus = InlineKeyboardMarkup(inline_keyboard=wh_bus)

hotel = [
    [
        InlineKeyboardButton(text="Усадьба"),
        InlineKeyboardButton(text="База отдыха"),
        InlineKeyboardButton(text="Аренда коттеджей")
    ],
    [
        InlineKeyboardButton(text="Гостевой дом"),
        InlineKeyboardButton(text="Турбаза"),
        InlineKeyboardButton(text="Шале")
    ]
]
hotel = InlineKeyboardMarkup(inline_keyboard=hotel)

service = [
    [
        InlineKeyboardButton(text="Рафтинг/сплавы"),
        InlineKeyboardButton(text="Квадроциклы")
    ],
    [
        InlineKeyboardButton(text="Гид"),
        InlineKeyboardButton(text="Маршрут"),
        InlineKeyboardButton(text="Экскурсия")
    ]
]
service = InlineKeyboardMarkup(inline_keyboard=service)


check = [
    [
        InlineKeyboardButton(text="Продолжить", callback_data="continue"),
        InlineKeyboardButton(text="Отмена", callback_data="back")
    ]
]
check = InlineKeyboardMarkup(inline_keyboard=check)

rmk = ReplyKeyboardRemove()

da = [
    [
        InlineKeyboardButton(text = "Да", callback_data="da")
    ]
]
da = InlineKeyboardMarkup(inline_keyboard=da)
