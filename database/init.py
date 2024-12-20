from tortoise import Tortoise

from config import settings


async def init_database() -> None:
    await Tortoise.init(
        db_url=settings.DB_URL.get_secret_value(),
        modules={"models": ["database.models"]}
    )
    await Tortoise.generate_schemas()


async def close_database() -> None:
    await Tortoise.close_connections()
