from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.filters import IsPrivate

router = Router()


@router.message(IsPrivate(), CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer('<b>🏠 Добро пожаловать! Вы находитесь в главном меню.</b>')


@router.callback_query(F.data == "menu")
async def call_menu(call: CallbackQuery) -> None:
    await call.message.edit_text('<b>🏠 Добро пожаловать! Вы находитесь в главном меню.</b>')
