from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import AdminFilter
from keyboards.inline.week_keyboards import week_cd, markup


from loader import db, dp
from states.AddTodoState import AddTodo


@dp.message_handler(AdminFilter(), commands="admin")
async def show_admin_panel(message: types.Message):
    await message.answer(
        "/add - yangi reja qo'shish\n"
        "/todos - barcha rejalar\n"
        "/clear_todos - todolarni tozalash"
    )




@dp.message_handler(AdminFilter(),commands="add")
async def start_add_todo(message: types.Message):
    await message.answer("Hafta kunlaridan birini tanlang", reply_markup=markup)
    await AddTodo.week.set()

@dp.message_handler(AdminFilter(), state=AddTodo.week)
async def unknown_command(message: types.Message):
    await message.delete()
    await message.answer("Nomalum buyruq")

@dp.callback_query_handler(AdminFilter(), week_cd.filter(), state=AddTodo.week)
async def get_weekday(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    if callback_data.get("week") == "cancel":
        await state.finish()
        await call.message.edit_reply_markup()
        await call.answer("Bekor qilindi")
        return
    await call.answer(cache_time=30)
    weekday = callback_data.get("week")
    await state.update_data(week=weekday if weekday != "cancel" else weekday)

    await call.message.edit_text("Ish rejani yozing")
    await AddTodo.todo.set()



@dp.message_handler(AdminFilter(), state=AddTodo.todo)
async def get_todo_function(message: types.Message, state: FSMContext):
    await state.update_data(todo=message.text)

    async with state.proxy() as data:
        week = data.get("week")
        todo = data.get("todo")
        await state.finish()
    try:
        db.add_todo(
            week=week,
            todo=todo
        )
        await message.answer("Ma'lumotlar qabul qilindi!")
    except Exception as e:
        print("Todoni bazaga qo'shishda xatolik\{}".format(e))




@dp.message_handler(AdminFilter(), commands="todos")
async def show_todos_all(message: types.Message):
    todos = db.get_all_todos()
    for todo in todos:
        text = f"{todo[0]}\n"
        text += f"{todo[1]}\n\n"
        await message.answer(text)

@dp.message_handler(AdminFilter(), commands="clear_todos")
async def clear_todos_from_db(message: types.Message):
    try:
        db.drop_todos()
        await message.answer("Todo baza tozalandi")
    except Exception as e:
        await message.answer("Todo jadval tozalandi")
        print(e)