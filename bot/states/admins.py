from aiogram.fsm.state import State, StatesGroup


class Mailing(StatesGroup):
    media = State()
    keyboard = State()


class FindUser(StatesGroup):
    user = State()


class ChangeUserNote(StatesGroup):
    note = State()


class SendUserMessage(StatesGroup):
    message = State()


class AddAdLink(StatesGroup):
    title = State()