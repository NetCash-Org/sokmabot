import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from filters import IsPrivate
from keyboards.inline.admqosh import language
from loader import dp, bot, db

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.types import Message


@dp.message_handler(IsPrivate(), commands="start")
async def start(msg: types.Message):
    await msg.answer('''🇺🇿 Tilni tanlang
🇷🇺 Выберите язык
🇺🇸 Choose language''', reply_markup=language)

@dp.callback_query_handler(lambda query: query.data == "uz")
async def start_handler(message: Message):
    """Handle the /start command in private chats."""
    try:
        admin = 1933542476
        await db.add_admin(admin)
    except:
        print("admin borakan o'zi")

    try:
        await db.add_user(telegram_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)

    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="➕Guruhga qo'shish",
                                                   url=f"https://t.me/Karkidon_uz_bot?startgroup=true"))
    input_content = InputTextMessageContent(message_text="Click the button below to add the bot to a group.")
    result = InlineQueryResultArticle(
        id="1",
        title="Add Bot to Group",
        input_message_content=input_content,
        reply_markup=inline_keyboard
    )


    await bot.send_message(message.from_user.id, f"""Salom, men Karkidon botman
Meni shunchaki guruhinggizga qo'shing va men u yerda tartibni o'rnataman va so'kinganlarni jazolayman.

/set komandasidan so'ng kerakli raqamni kiriting va so'kingan odam shuncha vaqtga bloklanadi

Guruhga qo'shish uchun shunchaki quyidagi tugmani bosing.
""", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data == "ru")
async def start_handler(message: Message):
    """Handle the /start command in private chats."""
    try:
        admin = 1933542476
        await db.add_admin(admin)
    except:
        print("admin borakan o'zi")

    try:
        await db.add_user(telegram_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)

    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="➕Добавить в группу",
                                                   url=f"https://t.me/Karkidon_uz_bot?startgroup=true"))
    input_content = InputTextMessageContent(message_text="Click the button below to add the bot to a group.")
    result = InlineQueryResultArticle(
        id="1",
        title="Add Bot to Group",
        input_message_content=input_content,
        reply_markup=inline_keyboard
    )

    await bot.send_message(message.from_user.id, """Привет, я бот-Каркидон
Просто добавьте меня в свою группу и я буду следить за порядком и наказывать плохих парней.

Введите желаемое число после команды /set, и человек, который выругался, будет заблокирован на это время.

Просто нажмите кнопку ниже, чтобы добавиться в группу.

""", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda query: query.data == "en")
async def start_handler(message: Message):
    """Handle the /start command in private chats."""
    try:
        admin = 1933542476
        await db.add_admin(admin)
    except:
        print("admin borakan o'zi")

    try:
        await db.add_user(telegram_id=message.from_user.id,
                          full_name=message.from_user.full_name,
                          username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)

    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="➕Add to group",
                                                   url=f"https://t.me/Karkidon_uz_bot?startgroup=true"))
    input_content = InputTextMessageContent(message_text="Click the button below to add the bot to a group.")
    result = InlineQueryResultArticle(
        id="1",
        title="Add Bot to Group",
        input_message_content=input_content,
        reply_markup=inline_keyboard
    )

    await bot.send_message(message.from_user.id, """Hi, I'm a karkidon bot
Just add me to your group and I'll keep order and punish the bad guys.

Enter the desired number after the /set command, and the person who cursed will be blocked for that amount of time

Just click the button below to add to the group.

""", reply_markup=inline_keyboard)

