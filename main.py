import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares
from bot.utils.notify_admins import on_startup_notify, on_shutdown_notify
from config import settings
from database import init_database, close_database

bot = Bot(
    settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def on_startup(bot: Bot) -> None:
    await init_database()
    await on_startup_notify(bot)


async def on_shutdown(bot: Bot) -> None:
    await close_database()
    await on_shutdown_notify(bot)


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(setup_routers())
    setup_middlewares(dp, bot)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
