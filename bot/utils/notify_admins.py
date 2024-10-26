import logging

from aiogram import Bot

from config import admins_ids


async def on_startup_notify(bot: Bot) -> None:
    try:
        text = f"<b>✅Бот запущен</b>"
        await bot.send_message(chat_id=admins_ids[0],
                               text=text)
    except Exception as ex:
        logging.exception('Ошибка при отправке сообщения админу', exc_info=ex)


async def on_shutdown_notify(bot: Bot) -> None:
    try:
        text = f"<b>❌Бот остановлен</b>"
        await bot.send_message(chat_id=admins_ids[0],
                               text=text)
    except Exception as ex:
        logging.exception('Ошибка при отправке сообщения админу', exc_info=ex)