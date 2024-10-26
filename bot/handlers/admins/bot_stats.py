from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.builders import back_to_builder
from database.commands.user import count_users

router = Router()


@router.callback_query(F.data == "bot_stats")
async def bot_stats(call: CallbackQuery) -> None:
    users_count = await count_users()

    await call.message.edit_text(f'<b>Статистика бота:</b>\n\n'
                                 f'<i><b>Всего пользователей:</b> {users_count}</i>',
                                 reply_markup=back_to_builder("admin_panel"))