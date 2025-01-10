from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📢Рассылка", callback_data="mailing"),
        InlineKeyboardButton(text="📊Статистика", callback_data="bot_stats")
    ],
    [
        InlineKeyboardButton(text="🔍Найти пользователя", callback_data="find_user")
    ],
    [
        InlineKeyboardButton(text="‹ Главное меню", callback_data="menu")
    ]
])