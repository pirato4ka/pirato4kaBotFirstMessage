from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic_settings import SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]  # корень проекта

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    # дальше поля как у вас...


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")

    

    main_bot_username: str = Field(default="MyMainBot", alias="MAIN_BOT_USERNAME")
    main_bot_url: str = Field(default="", alias="MAIN_BOT_URL")

    first_comment_md: str = Field(
        default="*Связь с нами:* [@{main_bot_username}]({main_bot_url})",
        alias="FIRST_COMMENT_MD",
    )

    allowed_channel_ids: str = Field(default="", alias="ALLOWED_CHANNEL_IDS")

    db_path: str = Field(default="data/processed.sqlite3", alias="DB_PATH")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def allowed_channels(self) -> set[int]:
        raw = (self.allowed_channel_ids or "").strip()
        if not raw:
            return set()
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        return {int(x) for x in parts}

    @property
    def resolved_main_bot_url(self) -> str:
        # Если ссылка не задана — соберём из username
        if self.main_bot_url.strip():
            return self.main_bot_url.strip()
        return f"https://t.me/{self.main_bot_username}"

    album_single_comment: bool = Field(default=True, alias="ALBUM_SINGLE_COMMENT")

    class Config:
        env_file = ".env"
        extra = "ignore"