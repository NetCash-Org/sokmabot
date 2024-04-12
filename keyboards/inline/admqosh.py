from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

addAdm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕", callback_data="plus"),
            InlineKeyboardButton(text="➖", callback_data="minus")
        ],
    ])

language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="en")
        ],
    ])
