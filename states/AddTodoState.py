from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTodo(StatesGroup):
    week = State()
    time = State()
    todo = State()