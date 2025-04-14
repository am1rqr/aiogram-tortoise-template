import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from config import ADMINS_IDS


async def on_startup_notify(bot: Bot) -> None:
    try:
        text = "<b>✅ Бот запущен</b>"
        await bot.send_message(chat_id=ADMINS_IDS[0],
                               text=text)
    except TelegramAPIError as ex:
        logging.exception("Ошибка при отправке сообщения админу", exc_info=ex)


async def on_shutdown_notify(bot: Bot) -> None:
    try:
        text = "<b>❌ Бот остановлен</b>"
        await bot.send_message(chat_id=ADMINS_IDS[0],
                               text=text)
    except TelegramAPIError as ex:
        logging.exception("Ошибка при отправке сообщения админу", exc_info=ex)
