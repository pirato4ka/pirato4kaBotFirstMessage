from __future__ import annotations

import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher

from app.logging_config import setup_logging
from app.settings import Settings
from bot.routers import setup_routers
from bot.storage.processed_posts import ProcessedPostsRepo


async def main() -> None:
    settings = Settings()

    setup_logging(settings.log_level)

    Path("data").mkdir(parents=True, exist_ok=True)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    repo = ProcessedPostsRepo(settings.db_path)
    await repo.init()

    # Прокидываем зависимости в aiogram handlers через ключи
    dp["settings"] = settings
    dp["repo"] = repo

    dp.include_router(setup_routers())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())