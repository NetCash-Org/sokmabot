from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, CallbackQuery, \
    InlineKeyboardButton, InlineKeyboardMarkup

from filters import IsPrivate, AdminFilter
from keyboards.default.adminKeyb import panelAdm, addWord, cancelWord
from keyboards.inline.admqosh import addAdm
from keyboards.inline.guruhqosh import inline_keyboard_admin
from loader import dp, bot, db

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.types import Message, ReplyKeyboardRemove

from states.admState import addAdmSt, removeAdmSt, wordSt, removeSt


@dp.message_handler(AdminFilter(), CommandStart())
async def start_handler(message: Message):
    await bot.send_message(message.from_user.id, """Salom, men karkidon botman
Meni shunchaki guruhinggizga qo'shing va men uyerda tartibni o'rnataman va so'kinganlarni jazolayman.

Guruhga qo'shish uchun shunchaki quyidagi tugmani bosing.

Bot haqida ma'lumot: /help""", reply_markup=inline_keyboard_admin)


# Assuming `dp` is your Dispatcher instance

@dp.callback_query_handler(lambda query: query.data == "adminlar")
async def admin_panel(qry: CallbackQuery):
    await qry.message.answer("Quyidagi tugmalarni tanlang", reply_markup=panelAdm)


@dp.message_handler(AdminFilter(), text="📊Statistika")
async def stat(msg: types.Message):
    count = await db.count_users()
    group_count = await db.count_groups()
    await msg.answer(f"Botda:\nGuruhlar: {group_count}ta\nFoydalanuvchilar: {count}ta")


@dp.message_handler(AdminFilter(), text="🧑‍💻Adminlar")
async def admins(msg: types.Message):
    # Fetch the list of admin Telegram IDs from the database
    admin_ids = await db.get_admins()

    if admin_ids:
        # Convert the list of admin IDs to a string for display
        admin_list = "\n".join(f"{index + 1}. {admin_id}" for index, admin_id in enumerate(admin_ids))

        # Send the list of admins as a message
        await msg.answer(f"Adminlar:\n{admin_list}", reply_markup=addAdm)
    else:
        await msg.answer("Admin topilmadi")


@dp.callback_query_handler(lambda query: query.data == "plus")
async def admin_qosh(qry: CallbackQuery):
    await qry.message.edit_text("Admin qo'shish uchun qo'shmoqchi bo'lgan userning idsini kiriting")
    await addAdmSt.admId.set()


@dp.message_handler(state=addAdmSt.admId)
async def takeAdm(msg: types.Message, state: FSMContext):
    try:
        get_admin_id = int(msg.text)
        have_in_users = await db.select_user(telegram_id=get_admin_id)
        have_in_admins = await db.is_admin(get_admin_id)
        if have_in_users:
            if not have_in_admins:
                await db.add_admin(get_admin_id)
                await msg.answer(f"{get_admin_id} idlik odam adminlar qatoriga qo'shildi✅")
            else:
                await msg.answer("Bu user adminlar orasida mavjud")
        else:
            await msg.answer("Bu user bot foydalanuvchilari orasida mavjud emas❗")
    except:
        await msg.answer("Admin qo'shish uchun faqatgina o'sha userning idsini kiritishinggiz kerak🤓!")

    admin_ids = await db.get_admins()
    # Convert the list of admin IDs to a string for display
    admin_list = "\n".join(f"{index + 1}. {admin_id}" for index, admin_id in enumerate(admin_ids))

    # Send the list of admins as a message
    await msg.answer(f"Adminlar:\n{admin_list}", reply_markup=addAdm)
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == "minus")
async def admin_ayr(qry: CallbackQuery):
    await qry.message.edit_text("Kimni adminlar orasidan olib tashlamoqchisiz? IDsini kiriting😉")
    await removeAdmSt.admId.set()


@dp.message_handler(state=removeAdmSt.admId)
async def delete_adm(msg: types.Message, state: FSMContext):
    try:
        delId = int(msg.text)
        await db.remove_admin(delId)
        await msg.answer(f"{delId} idli odam adminlar orasidan chopildi☠️")
    except:
        await msg.answer("Bunday user adminlar orasida mavjud emas❌")

    admin_ids = await db.get_admins()
    # Convert the list of admin IDs to a string for display
    admin_list = "\n".join(f"{index + 1}. {admin_id}" for index, admin_id in enumerate(admin_ids))

    # Send the list of admins as a message
    await msg.answer(f"Adminlar:\n{admin_list}", reply_markup=addAdm)
    await state.finish()


@dp.message_handler(AdminFilter(), text="🤬Nomaqbul so'zlar ro'yhati")
async def send_bad_words_chunk(msg: types.Message):
    # Get all bad words from the database
    bad_words = await db.get_all_words()
    try:
        # Create a string to display the bad words with sequential numbers
        text = "So'kinishlar ro'yhati:\n"
        for index, word in enumerate(bad_words, start=1):
            text += f"{index}. {word}\n"
    except:
        text = "So'kinishlar mavjud emas"
    # Send the bad words list
    await msg.reply(text, reply_markup=addWord)

@dp.message_handler(text="➕Qo'shish")
async def newWordWith(msg: types.Message):
    await msg.answer("Qo'shmoqchi bo'lgan so'zinggizni kiriting.", reply_markup=cancelWord)
    await wordSt.addSt.set()

@dp.message_handler(text="❌Olib tashlash")
async def newWordWith(msg: types.Message):
    await msg.answer("Olib tashlamoqchi bo'lgan so'zingizni kiriting", reply_markup=cancelWord)
    await removeSt.remSt.set()

@dp.message_handler(state=wordSt.addSt, text="❌Qaytish")
@dp.message_handler(state=removeSt.remSt, text="❌Qaytish")
async def send_bad_words_back(msg, chunks, chunk_index):
    bad_words = await db.get_all_words()

    # If there are no bad words, inform the admin
    if not bad_words:
        await msg.reply("Hozircha nomaqbul so'zlar mavjud emas", reply_markup=addWord)
        return

    # Create a string to display the bad words with sequential numbers
    text = "So'kinishlar ro'yhati:\n"
    for index, word in enumerate(bad_words, start=1):
        text += f"{index}. {word}\n"

    # Send the bad words list
    await msg.reply(text, reply_markup=addWord)

@dp.message_handler(state=wordSt.addSt)
async def addNewWord(msg: types.Message, state: FSMContext):
    new_word = msg.text.strip()  # Remove leading and trailing whitespaces

    # Check if the number of words in the input is more than 1
    if len(new_word.split()) > 1:
        await msg.answer("So'z faqat 1 ta so'zdan iborat bo'lishi kerak", reply_markup=cancelWord)
        # Finish the state machine without attempting to add the word to the database
        return

    # Try to add the new word to the database
    if await db.add_word(new_word):
        # If the word was successfully added, send a success message
        await msg.answer("So'z muvaffaqiyatli qo'shildi", reply_markup=panelAdm)
    else:
        # If the word already exists, send an error message
        await msg.answer("Bu so'z allaqachon qo'shilgan", reply_markup=panelAdm)

    # Finish the state machine
    await state.finish()





@dp.message_handler(AdminFilter(), text="🔙Ortga qaytish")
async def back(msg: types.Message):
    await msg.answer("Siz bosh menyudasiz", reply_markup=panelAdm)

@dp.message_handler(state=removeSt.remSt)
async def addNewWord(msg: types.Message, state: FSMContext):
    new_word = msg.text

    # Try to add the new word to the database
    try:
        await db.delete_word(new_word)
        # If the word was successfully added, send a success message
        await msg.answer("So'z muvaffaqiyatli o'chirildi", reply_markup=panelAdm)
    except:
        # If the word already exists, send an error message
        await msg.answer("Bunday so'z mavjud emas", reply_markup=panelAdm)

    # Finish the state machine
    await state.finish()