import os

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

admins_ids = [1026603474, 2, 3]  # Первому админу будут приходить уведомления

timezone = "Asia/Almaty"  # Часовой пояс
tz_info = "AST"  # Для вывода в сообщениях