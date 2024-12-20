from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.builders import back_to_builder
from database.commands.user import timely_count_users, all_time_count_users

router = Router()


@router.callback_query(F.data == "bot_stats")
async def bot_stats(call: CallbackQuery) -> None:
    one_day_count = await timely_count_users(1)
    one_week_count = await timely_count_users(7)
    one_month_count = await timely_count_users(30)
    one_year_count = await timely_count_users(365)
    all_time_count = await all_time_count_users()

    await call.message.edit_text(f"📊 Статистика бота:\n\n"
                                 f"📈 Количество пользователей:\n"
                                 f"• За сегодня: {one_day_count}\n"
                                 f"• За неделю: {one_week_count}\n"
                                 f"• За месяц: {one_month_count}\n"
                                 f"• За год: {one_year_count}\n"
                                 f"• За все время: {all_time_count}",
                                 reply_markup=back_to_builder("admin_panel"))