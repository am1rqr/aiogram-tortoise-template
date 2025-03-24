import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union

from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    TelegramObject,
)

DEFAULT_DELAY = 0.6


class AlbumMiddleware(BaseMiddleware):
    """
    Usage:
        async def handler(message: Message, album: list[Message] = None) -> None:
    """
    ALBUM_DATA: Dict[str, List[Message]] = {}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(DEFAULT_DELAY)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)
