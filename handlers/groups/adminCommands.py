import asyncio

import aiogram

from filters import IsGroup
from loader import dp, bot, db
from aiogram import types


async def is_user_admin(chat_id, user_id):
    # Get chat member information
    chat_member = await bot.get_chat_member(chat_id, user_id)

    # Check if the user is an administrator
    return chat_member.is_chat_admin()



@dp.message_handler(IsGroup(), commands=['set'])
async def handle_add_command(message: types.Message):
    if await is_user_admin(message.chat.id, message.from_user.id):
        # Split the message text into command and argument
        try:
            command, argument = message.text.split(maxsplit=1)
        except ValueError:
            await message.reply("Userlar so'kinganda qancha vaqtga bloklanishini belgilash uchun /set komandasidan foydalaning. "
                                "\nMasalan, /set 5"
                                "\nBu holatda foydalanuvchi so'kinsa 5 minutga bloklanadi."
                                "\n\nBotni to'xtatish uchun shunchaki /set 0 yozing.")
            return

        group_id = str(message.chat.id)

        # Check if the argument is a number
        try:
            number = int(argument)
            if number == 0:
                # Disable message checking by setting restrict_min to 0
                await db.update_restrict_min_by_group_id(number, group_id)
                await message.reply("Bot faoliyati yakunlandi.")
            else:
                # Update the restrict_min value with the provided number of minutes
                await db.update_restrict_min_by_group_id(number, group_id)
                await message.reply(
                    f"Cheklov qo'yildi. Endilikda userlar so'kinsa {number} minutga bloklanadi.")
        except ValueError:
            await message.reply("Userlar so'kinganda qancha vaqtga bloklanishini belgilash uchun /set komandasidan foydalaning. "
                                "\nMasalan, /set 5"
                                "\nBu holatda foydalanuvchi so'kinsa 5 minutga bloklanadi."
                                "\n\nBotni to'xtatish uchun shunchaki /set 0 yozing.")
        except Exception as e:
            print(e)
