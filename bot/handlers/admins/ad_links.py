from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.builders import ad_links_builder
from database.commands.ad_links import get_all_links

router = Router()


@router.callback_query(F.data == "ad_links")
async def call_add_links(call: CallbackQuery) -> None:
    all_ad_links = await get_all_links()
    await call.message.edit_text("<b>📎 Рекламные ссылки:</b>",
                                 reply_markup=ad_links_builder(all_ad_links))