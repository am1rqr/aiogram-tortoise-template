from typing import Callable, Any, Dict, Union, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from database.commands.user import select_user_by_id
from database.models import Users


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        current_event = event.message or event.callback_query
        if not current_event:
            return await handler(event, data)

        user = await select_user_by_id(current_event.from_user.id)
        data["is_first_time"] = False
        if not user:
            user = await Users.create(user_id=current_event.from_user.id,
                                      username=current_event.from_user.username)
            data["is_first_time"] = True

        if user.username != current_event.from_user.username:
            user.username = current_event.from_user.username
            await user.save()

        data['user'] = user
        return await handler(event, data)