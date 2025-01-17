from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def find_user_builder(user_status: str, user_id: int) -> InlineKeyboardMarkup:
    if user_status == "active":
        button_text = "🔒 Заблокировать"
    else:
        button_text = "🔓 Разблокировать"

    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="📝 Изменить заметку", callback_data=f"change_user_note#{user_id}")
    keyboard_builder.button(text=button_text, callback_data=f"change_user_status#{user_id}")
    keyboard_builder.button(text="‹ Назад", callback_data="find_user")

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()