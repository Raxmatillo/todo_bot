import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        db.add_user(
            id=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username
        )
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}")
    except sqlite3.IntegrityError as e:
        await bot.send_message(ADMINS[0], text=f"{e}")

    await message.answer("Xush kelibsiz")