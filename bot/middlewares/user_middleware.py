from datetime import datetime
from typing import Callable, Any, Dict, Union, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from database.commands.user import select_user_by_id, update_user_last_activity, update_user_username
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

        data["is_first_time"] = False
        user = await select_user_by_id(current_event.from_user.id)
        if not user:
            user = await Users.create(user_id=current_event.from_user.id,
                                      username=current_event.from_user.username,
                                      first_name=current_event.from_user.first_name)
            data["is_first_time"] = True

        await update_user_last_activity(user.user_id)
        if user.username != current_event.from_user.username:
            await update_user_username(user.user_id, current_event.from_user.username)

        if user.status == "banned":
            return

        data['user'] = user
        return await handler(event, data)
