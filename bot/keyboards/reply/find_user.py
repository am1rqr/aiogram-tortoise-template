from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser

find_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍 Выбрать пользователя",
                           request_user=KeyboardButtonRequestUser(
                               request_id=1,
                               user_is_bot=False
                           ))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
