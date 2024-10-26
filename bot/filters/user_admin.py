from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import admins_ids


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in admins_ids