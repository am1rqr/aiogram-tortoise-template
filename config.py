import os

import pytz
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore

ADMINS_IDS = [1, 2, 3]  # Первому админу будут приходить уведомления

TIMEZONE = "Asia/Almaty"  # Часовой пояс
TZ_INFO = "AST"  # Для вывода в сообщениях
tz = pytz.timezone(TIMEZONE)