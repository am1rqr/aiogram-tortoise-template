import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from bot.handlers import setup_routers
from bot.utils.notify_admins import on_startup_notify, on_shutdown_notify
from config import settings

bot = Bot(
        settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
dp = Dispatcher()


async def on_startup(bot: Bot) -> None:
    await Tortoise.init(
        db_url=settings.DB_URL.get_secret_value(),
        modules={"models": ["database.models"]}
    )
    await Tortoise.generate_schemas()

    await on_startup_notify(bot)


async def on_shutdown(bot: Bot) -> None:
    await Tortoise.close_connections()
    await on_shutdown_notify(bot)


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(setup_routers())

    from bot.middlewares import UserMiddleware, ErrorMiddleware
    dp.callback_query.middleware(ErrorMiddleware(bot))
    dp.message.middleware(ErrorMiddleware(bot))
    dp.update.middleware(UserMiddleware())

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот был остановлен пользователем.")
    except Exception as e:
        logging.exception(f"Произошла непредвиденная ошибка: {e}")