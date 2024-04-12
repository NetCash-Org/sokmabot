from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        admins = await db.get_admins()

        if message.chat.id in admins:
            return True
        else:
            return False
