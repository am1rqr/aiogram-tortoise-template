from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.builders import approval_builder, back_to_builder
from database.commands.ad_links import delete_ad_link

router = Router()


@router.callback_query(F.data == "delete_ad_link")
async def call_delete_ad_link(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    ad_link_id: int = data.get("ad_link_id")
    ad_link_title: str = data.get("ad_link_title")

    await call.message.edit_text(f'<i>❓Вы действительно хотите удалить рекламную ссылку "{ad_link_title}"?</i>',
                                 reply_markup=approval_builder("approval_delete_ad_link", "ad_links"))


@router.callback_query(F.data == "approval_delete_ad_link")
async def call_approval_delete_ad_link(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    ad_link_id: int = data.get("ad_link_id")

    await delete_ad_link(ad_link_id)

    await call.message.edit_text("<b>✅ Рекламная ссылка успешно удалена!</b>",
                                 reply_markup=back_to_builder("ad_links"))
    await state.clear()