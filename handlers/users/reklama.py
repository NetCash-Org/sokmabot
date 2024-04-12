import asyncio

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import AdminFilter
from keyboards.default.adminKeyb import atmenql, panelAdm
from loader import dp, db, bot
from states.admState import rek


@dp.message_handler(AdminFilter(), text="®️Reklama Yuborish")
async def reksendd(msg: types.Message):
    await msg.answer("Userlarga va guruhlarga jo'natmoqchi bo'lgan reklamangizni kiriting✅", reply_markup=atmenql)
    await rek.sendrek.set()

@dp.message_handler(state=rek.sendrek, text="❌Bekor qilish")
async def atmenfunc(msg: types.Message,  state: FSMContext):
    await msg.answer("Reklama bekor qilindi❌", reply_markup=panelAdm)
    await state.finish()


@dp.message_handler(state=rek.sendrek, content_types=types.ContentType.ANY)
async def rekhabar(msg: types.Message, state: FSMContext):
    count = await db.count_users()
    if count > 100:
        await msg.answer("🕟Habaringgiz barcha obunachilar va guruhlarga yuborilmoqda...")
    # Retrieve all users and unique group IDs
    users = await db.select_all_users()
    groups = await db.get_unique_group_ids()
    ozhabarim = msg.from_user.id
    # Forward the message to all users
    for user in users:
        try:
            user_id = user[3]
            if user_id == msg.from_user.id:
                continue
            await bot.forward_message(chat_id=user_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
            await asyncio.sleep(0.05)
        except aiogram.exceptions.ChatNotFound:
            print(f"Chat not found. Skipping.")
        except Exception as e:
            print(f"Failed to forward message to user: {e}")

    # Forward the message to all groups
    for group in groups:
        group_id = group[0]
        try:
            await bot.forward_message(chat_id=group_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
            await asyncio.sleep(0.05)
        except aiogram.exceptions.ChatNotFound:
            print(f"Chat not found for group {group_id}. Skipping.")
        except Exception as e:
            print(f"Failed to forward message to group {group_id}: {e}")

    await msg.answer("Habaringgiz barcha obunachilar va guruhlarga yuborildi✅", reply_markup=panelAdm)
    # Finish the state machine
    await state.finish()