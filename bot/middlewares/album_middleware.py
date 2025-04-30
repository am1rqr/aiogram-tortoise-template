import asyncio
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    TelegramObject,
)

DEFAULT_DELAY = 0.6


class AlbumMiddleware(BaseMiddleware):
    """
    Usage:
        async def handler(message: Message, album: list[Message] = None):
    """
    ALBUM_DATA: dict[str, list[Message]] = {}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return None
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(DEFAULT_DELAY)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)
