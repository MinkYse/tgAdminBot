from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

def profile(text: str | list):
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt, callback_data=f"{txt}") for txt in text]
    return builder.as_markup()

def create_keyboard(data: list):
    inline_list = []
    for el in data:
        inline_list.append([InlineKeyboardButton(text=el, callback_data=el)])
    my_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_list
    )
    return my_keyboard