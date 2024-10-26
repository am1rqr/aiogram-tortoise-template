from aiogram.fsm.state import State, StatesGroup


class Mailing(StatesGroup):
    media = State()
    keyboard = State()