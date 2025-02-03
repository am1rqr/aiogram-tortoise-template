import random
import string

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_start_link

from bot.keyboards.builders import ad_links_builder, back_to_builder
from bot.states.admins import AddAdLink
from database.commands.ad_links import get_all_links, add_ad_link

router = Router()


@router.callback_query(F.data == "ad_links")
async def call_ad_links(call: CallbackQuery) -> None:
    all_ad_links = await get_all_links()
    await call.message.edit_text("<b>📎 Рекламные ссылки:</b>",
                                 reply_markup=ad_links_builder(all_ad_links))


@router.callback_query(F.data == "add_ad_link")
async def call_add_ad_link(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text("<b>✍️ Введите название ссылки:</b>",
                                 reply_markup=back_to_builder("ad_links"))
    await state.set_state(AddAdLink.title)


@router.message(AddAdLink.title)
async def get_ad_link_title(message: Message, state: FSMContext, bot: Bot) -> None:
    code = get_random_string()
    await add_ad_link(message.text, code)

    link = await create_start_link(bot, code)
    await message.answer(f"<b>📎 {message.text}</b>\n\n"
                         f"<code>{link}</code>",
                         reply_markup=back_to_builder("ad_links"))


def get_random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=6))