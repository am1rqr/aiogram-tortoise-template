from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def button_builder(text: str, callback_data: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=text,
                            callback_data=callback_data)

    return keyboard_builder.as_markup()
