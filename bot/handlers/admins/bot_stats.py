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
    all_time_count = await all_time_count_users()

    await call.message.edit_text(f"<b>📊 Статистика бота:</b>\n\n"
                                 f"<b>📈 Количество пользователей:</b>\n"
                                 f"<b>• За сегодня: <i>{one_day_count}</i></b>\n"
                                 f"<b>• За неделю: <i>{one_week_count}</i></b>\n"
                                 f"<b>• За месяц: <i>{one_month_count}</i></b>\n"
                                 f"<b>• За все время: <i>{all_time_count}</i></b>",
                                 reply_markup=back_to_builder("admin_panel"))