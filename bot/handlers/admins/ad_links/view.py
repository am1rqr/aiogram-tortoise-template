from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from bot.keyboards.builders import ad_links_builder, ad_links_view_builder
from config import tz
from database.commands.ad_links import get_all_active_ad_links, get_ad_link_by_id

router = Router()


@router.callback_query(F.data == "ad_links")
async def call_ad_links(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    all_ad_links = await get_all_active_ad_links()
    await call.message.edit_text("<b>📎 Рекламные ссылки:</b>",
                                 reply_markup=ad_links_builder(all_ad_links))


@router.callback_query(F.data.startswith("ad_link#"))
async def call_ad_link(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    ad_link_id = int(call.data.split("#")[1])
    ad_link = await get_ad_link_by_id(ad_link_id)

    link = await create_start_link(bot, ad_link.code)
    created_date = ad_link.created_at.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")

    await call.message.edit_text(f"<b>📌 {ad_link.title}</b>\n\n"
                                 f"<b><i>🚪 Всего посещений: {ad_link.total_visits}</i></b>\n"
                                 f"<b><i>👤 Уникальных посещений: {ad_link.unique_visits}</i></b>\n\n"
                                 f"<i>📅 Дата создания: {created_date}</i>\n\n"
                                 f"<code>{link}</code>\n\n",
                                 reply_markup=ad_links_view_builder(ad_link_id))

    await state.update_data(ad_link_id=ad_link_id,
                            ad_link_title=ad_link.title)