import datetime

import asyncpg
from aiogram import types

from filters import IsGroup
from loader import dp, db, bot


async def is_user_admin(chat_id, user_id):
    # Get chat member information
    chat_member = await bot.get_chat_member(chat_id, user_id)

    # Check if the user is an administrator
    return chat_member.is_chat_admin()


@dp.message_handler(IsGroup(), content_types=types.ContentType.TEXT)
async def check_message_for_bad_words(message: types.Message):
    # Get all bad words from the database
    bad_words = await db.get_all_words()
    user_id = message.from_user.id

    try:
        restMin = 5
        await db.add_new_group(str(message.chat.id), restMin)
        print("bu guruh qo'shildi")
    except asyncpg.exceptions.UniqueViolationError:
        print("bu guruh bor")

    # Fetch restrict minutes for the group
    minut = await db.get_restrict_min_by_group_id(str(message.chat.id))
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=minut)

    # Check if minut is None before using it
    if minut is None:
        print("Minut is None")
        return

    if minut <= 0:
        print("Minut is 0")
        return

    is_admin = await is_user_admin(message.chat.id, message.from_user.id)

    # Check if the message contains any bad words
    for word in bad_words:
        if word.lower() in message.text.lower():
            if not is_admin:
                # Send a warning message to the user
                await message.delete()
                await message.answer(f"{message.from_user.get_mention(as_html=True)}, siz guruhda so'kinganinggiz uchun {minut} minutga guruhda bloklandingiz")
                user_allowed = types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_invite_users=True,  # Allow adding contacts
                    can_change_info=False,
                    can_pin_messages=False,
                )
                await message.chat.restrict(user_id=user_id, permissions=user_allowed, until_date=until_date)
                return  # Exit the loop if a bad word is found
            else:
                await message.delete()
                await message.answer("Admin bo'lsangiz ham iltimos so'kinmasdan gapiring")
