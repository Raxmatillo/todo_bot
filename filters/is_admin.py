from aiogram import types
from aiogram.dispatcher.filters import Filter
from data.config import ADMINS


class AdminFilter(Filter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in str(ADMINS)


