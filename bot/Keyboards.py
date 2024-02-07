from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Размещение")],
        [KeyboardButton(text="Услуга")]
    ],
    resize_keyboard=True
)

hotel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Усадьба"),
            KeyboardButton(text="База отдыха"),
            KeyboardButton(text="Аренда коттеджей")
        ],
        [
            KeyboardButton(text="Гостевой дом"),
            KeyboardButton(text="Турбаза"),
            KeyboardButton(text="Шал*")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рафтинг/сплавы"),
            KeyboardButton(text="Квадроциклы")
        ],
        [
            KeyboardButton(text="Гид"),
            KeyboardButton(text="Маршрут"),
            KeyboardButton(text="Экскурсия")
        ]
    ],
    resize_keyboard=True
)

rmk = ReplyKeyboardRemove()