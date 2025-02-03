from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import AdLinks


def ad_links_builder(all_ad_links: list[AdLinks]) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    add_ad_link_button = InlineKeyboardButton(text="➕Добавить ссылку", callback_data="add_ad_link")
    keyboard_builder.row(add_ad_link_button)

    buttons = [
        InlineKeyboardButton(text=ad_link.title, callback_data=f"ad_link#{ad_link.id}")
        for ad_link in all_ad_links
    ]

    for i in range(0, len(buttons), 2):
        keyboard_builder.row(*buttons[i:i + 2])

    return keyboard_builder.as_markup()
