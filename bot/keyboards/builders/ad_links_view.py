from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ad_links_view_builder(ad_link_id) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🗑 Удалить", callback_data="delete_ad_link")
    keyboard_builder.button(text='‹ Назад', callback_data="ad_links")

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
