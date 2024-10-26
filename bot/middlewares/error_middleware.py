from typing import Any, Callable, Dict, Awaitable, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery
import logging


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
        except Exception as ex:
            logging.error(ex)

            await self.bot.send_message(chat_id=event.from_user.id,
                                        text=f"<b>❗️Произошла неизвестная ошибка:</b>\n"
                                             f"<i>{ex}</i>")