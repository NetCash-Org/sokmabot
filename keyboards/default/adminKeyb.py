from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

panelAdm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧑‍💻Adminlar"),
        ],
        [
            KeyboardButton(text="®️Reklama Yuborish"),
            KeyboardButton(text="📊Statistika")
        ],
        [
            KeyboardButton(text="🤬Nomaqbul so'zlar ro'yhati")
        ],
    ],
    resize_keyboard=True
)

atmenql = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Bekor qilish")
        ]
    ],
    resize_keyboard=True
)

addWord = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕Qo'shish"),
            KeyboardButton(text="❌Olib tashlash")
        ],
        [
            KeyboardButton(text="🔙Ortga qaytish")
        ]
    ],
    resize_keyboard=True
)

cancelWord = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Qaytish")
        ]
    ],
    resize_keyboard=True
)
