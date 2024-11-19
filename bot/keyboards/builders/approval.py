from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def approval_builder(approval: str, cancel: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✅Подтвердить', callback_data=approval)
    keyboard_builder.button(text='❌Отменить', callback_data=cancel)

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(row_width=1)
