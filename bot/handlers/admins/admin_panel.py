from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.filters import IsPrivate, IsAdmin
from bot.keyboards.inline import admin_panel_kb

router = Router()


@router.message(IsPrivate(), IsAdmin(), Command("admin"))
async def cmd_admin_panel(message: Message) -> None:
    await message.answer("Админ панель",
                         reply_markup=admin_panel_kb)


@router.callback_query(F.data == "admin_panel")
async def call_admin_panel(call: CallbackQuery) -> None:
    await call.message.edit_text("Админ панель",
                                 reply_markup=admin_panel_kb)