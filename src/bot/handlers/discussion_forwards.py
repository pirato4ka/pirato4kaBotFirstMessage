from __future__ import annotations

import logging

from aiogram import Router
from aiogram.types import Message, MessageOriginChannel

from app.settings import Settings
from bot.services.first_comment import post_first_comment
from bot.storage.processed_posts import ProcessedPostsRepo

log = logging.getLogger(__name__)
router = Router()


def extract_origin_channel(message: Message) -> tuple[int, int] | None:
    # Для авто-пересланных сообщений из канала в discussion group
    if not message.is_automatic_forward:
        return None

    # Новый формат (Bot API): forward_origin
    if isinstance(message.forward_origin, MessageOriginChannel):
        return message.forward_origin.chat.id, message.forward_origin.message_id

    # На всякий случай старые поля, если вдруг доступны
    if message.forward_from_chat and message.forward_from_message_id:
        return message.forward_from_chat.id, message.forward_from_message_id

    return None


@router.message()
async def on_discussion_auto_forward(
    message: Message,
    settings: Settings,
    repo: ProcessedPostsRepo,
) -> None:
    origin = extract_origin_channel(message)
    if not origin:
        return

    channel_id, channel_message_id = origin

    allowed = settings.allowed_channels
    if allowed and channel_id not in allowed:
        return

    # альбомы: 1 комментарий на media_group_id
    if settings.album_single_comment and message.media_group_id:
        if await repo.is_media_group_processed(channel_id, message.media_group_id):
            return

    # дедуп по посту
    if await repo.is_processed(channel_id, channel_message_id):
        return

    # пробуем отправить
    await post_first_comment(message.bot, settings, message)

    # помечаем как обработанное ПОСЛЕ успешной отправки
    await repo.mark_processed(channel_id, channel_message_id)
    if settings.album_single_comment and message.media_group_id:
        await repo.mark_media_group_processed(channel_id, message.media_group_id)

    log.info("First comment posted for channel=%s post=%s", channel_id, channel_message_id)