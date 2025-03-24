from aiogram import Bot, Dispatcher

from .album_middleware import AlbumMiddleware
from .error_middleware import ErrorMiddleware
from .user_middleware import UserMiddleware


def setup_middlewares(dp: Dispatcher, bot: Bot) -> None:
    dp.callback_query.middleware(ErrorMiddleware(bot))
    dp.message.middleware(ErrorMiddleware(bot))
    dp.message.middleware(AlbumMiddleware())
    dp.update.middleware(UserMiddleware())