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


def create_admin_keyboard(id, type):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Согласовать', callback_data=f'agree-{id}-{type}')],
            [InlineKeyboardButton(text='Отказать', callback_data=f'discard-{id}-{type}')]
        ]
    )
    return keyboard


def client_keyboard(user_id, product_id, position):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Согласовать', callback_data=f'offer-{user_id}-{product_id}-{position}')]
        ]
    )
    return keyboard


def confirm_keyboard(user_id, user_name, position):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm-{user_id}-{user_name}-{position}')]
        ]
    )
    return keyboard
