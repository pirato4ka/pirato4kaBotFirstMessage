from __future__ import annotations

import logging
from aiogram import Router
from aiogram.types import Message

from app.settings import Settings
from bot.services.first_comment import post_first_comment
from bot.storage.processed_posts import ProcessedPostsRepo

log = logging.getLogger(__name__)
router = Router()


@router.channel_post()
async def on_new_channel_post(message: Message, settings: Settings, repo: ProcessedPostsRepo) -> None:
    channel_id = message.chat.id

    allowed = settings.allowed_channels
    if allowed and channel_id not in allowed:
        return

    # 1) Защита от дублей для альбомов: 1 комментарий на media_group_id
    if settings.album_single_comment and message.media_group_id:
        if await repo.is_media_group_processed(channel_id, message.media_group_id):
            return
        # отмечаем альбом обработанным сразу
        await repo.mark_media_group_processed(channel_id, message.media_group_id)

    # 2) Дедуп для одиночных сообщений (и на всякий случай)
    if await repo.is_processed(channel_id, message.message_id):
        return
    await repo.mark_processed(channel_id, message.message_id)

    try:
        await post_first_comment(message.bot, settings, message)
    except Exception:
        log.exception("Unexpected error while posting first comment.")