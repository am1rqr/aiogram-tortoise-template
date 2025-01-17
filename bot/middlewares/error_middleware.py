import html
import logging
import traceback
from typing import Any, Callable, Dict, Awaitable, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery

from config import admins_ids


class ErrorMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as ex:  # noqa
            error_trace = traceback.format_exc()
            logging.error(error_trace)

            await self.bot.send_message(event.from_user.id,
                                        f"<b>❗️Произошла неизвестная ошибка, попробуйте позже.</b>")

            user_id = event.from_user.id
            username = event.from_user.username
            user_info = f"@{username} | {user_id}" if username else f"ID {user_id}"

            await self.bot.send_message(admins_ids[0],
                                        f"<b>❗️Произошла неизвестная ошибка у пользователя {user_info}:</b>\n\n"
                                        f"<pre>{html.escape(error_trace)}</pre>")