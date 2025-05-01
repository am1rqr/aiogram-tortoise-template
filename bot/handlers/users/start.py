from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.filters import IsPrivate
from database.commands.ad_links import get_ad_link_by_code, add_total_visits, add_unique_visits

router = Router()


@router.message(IsPrivate(), CommandStart())
async def cmd_start(message: Message, command: CommandObject, is_first_time: bool) -> None:
    args = command.args
    if args:
        await handle_ad_link_visit(args, is_first_time)

    await message.answer("<b>🏠 Добро пожаловать! Вы находитесь в главном меню.</b>")


async def handle_ad_link_visit(code: str, is_first_time: bool) -> None:
    ad_link = await get_ad_link_by_code(code)
    if not ad_link:
        return

    await add_total_visits(ad_link.id)

    if is_first_time:
        await add_unique_visits(ad_link.id)


@router.callback_query(F.data == "menu")
async def call_menu(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("<b>🏠 Добро пожаловать! Вы находитесь в главном меню.</b>")