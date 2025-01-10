from aiogram.fsm.state import State, StatesGroup


class Mailing(StatesGroup):
    media = State()
    keyboard = State()


class FindUser(StatesGroup):
    user = State()