import asyncio
import calendar

from aiogram import executor
from data.config import ADMINS
from datetime import date
import aioschedule
from loader import dp, bot, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


my_date = date.today()
week_name = calendar.day_name[my_date.weekday()].lower()
get_todo_from_db = db.get_todo_by_week(week=week_name)

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    # db.drop_todos()
    # db.create_table_users()
    # db.create_table_todos()
    await on_startup_notify(dispatcher)
    asyncio.create_task(daily_tasks())


async def send_message(text):
    users = db.select_all_users()
    try:
        for user in users:
            await bot.send_message(chat_id=user[0], text=text)
    except Exception as err:
        await bot.send_message(ADMINS[0], text=err)


async def week_function():
    text = get_todo_from_db[0][1]
    await send_message(text)


async def daily_tasks():
    aioschedule.every().day.at("06:00").do(week_function)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

# data = {
#     "0": "Monday",
#     "1": "Tuesday",
#     "2": "Wednesday",
#     "3": "Thursday",
#     "4": "Friday",
#     "5": "Saturday",
#     "6": "Sunday"
# }

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)