from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters import AdminFilter, IsPrivate
from loader import dp, db


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "Dasturchi: @sXasanov")
    
    await message.answer("\n".join(text))

@dp.message_handler(IsPrivate(), commands="set")
async def set(msg: types.Message):
    await msg.answer("Bu komanda faqat guruhda ishlatiladi")

@dp.message_handler(AdminFilter(), commands="delete_words")
async def drop_table(msg: types.Message):
    await db.delete_words()
    await msg.answer("So'zlar tozalandi")

#drop group handler
@dp.message_handler(AdminFilter(), commands="drop_group")
async def drop_group(msg: types.Message):
    await db.drop_groups()
    await msg.answer("Guruhlar tozalandi")

@dp.message_handler(AdminFilter(), commands="min")
async def min(msg: types.Message):
    minut = await db.get_restrict_min_by_group_id(str(msg.chat.id))
    await msg.answer(str(minut))  # Sending minut as plain text

