from aiogram.enums import ParseMode

def escape_md2_text(s: str) -> str:
    for ch in r"_*[]()~`>#+-=|{}.!":
        s = s.replace(ch, "\\" + ch)
    return s

def escape_md2_url(s: str) -> str:
    # В URL внутри (...) в MarkdownV2 критичны "\" и ")"
    return s.replace("\\", "\\\\").replace(")", "\\)")

async def post_first_comment(bot, settings, discussion_root):
    text = settings.first_comment_md.format(
        main_bot_username=escape_md2_text(settings.main_bot_username),
        main_bot_url=escape_md2_url(settings.resolved_main_bot_url),
    )

    await bot.send_message(
        chat_id=discussion_root.chat.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
        reply_to_message_id=discussion_root.message_id,
        message_thread_id=discussion_root.message_thread_id if discussion_root.message_thread_id else None,
    )