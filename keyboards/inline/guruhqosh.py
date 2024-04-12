from aiogram import types

inline_keyboard_admin = types.InlineKeyboardMarkup()
inline_keyboard_admin.add(types.InlineKeyboardButton(text="➕Guruhga qo'shish",
                                               url=f"https://t.me/Karkidon_uz_bot?startgroup=true"))

# New inline keyboard button
inline_keyboard_admin.add(types.InlineKeyboardButton(text="Admin panel",
                                               callback_data="adminlar"))

input_content = types.InputTextMessageContent(message_text="Click the button below to add the bot to a group.")
result = types.InlineQueryResultArticle(
    id="1",
    title="Add Bot to Group",
    input_message_content=input_content,
    reply_markup=inline_keyboard_admin
)

inline_keyboard = types.InlineKeyboardMarkup()
inline_keyboard.add(types.InlineKeyboardButton(text="➕Guruhga qo'shish",
                                               url=f"https://t.me/Karkidon_uz_bot?startgroup=true"))

# New inline keyboard button
inline_keyboard.add(types.InlineKeyboardButton(text="Admin panel",
                                               callback_data="adminlar"))

input_content = types.InputTextMessageContent(message_text="Click the button below to add the bot to a group.")
results = types.InlineQueryResultArticle(
    id="1",
    title="Add Bot to Group",
    input_message_content=input_content,
    reply_markup=inline_keyboard
)