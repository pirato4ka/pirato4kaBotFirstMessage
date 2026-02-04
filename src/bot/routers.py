from aiogram import Router

#from bot.handlers.channel_posts import router as channel_posts_router
from bot.handlers.start import router as start_router
from bot.handlers.discussion_forwards import router as discussion_forwards_router

def setup_routers() -> Router:
    root = Router()
    root.include_router(start_router)
 #   root.include_router(channel_posts_router)
    root.include_router(discussion_forwards_router)
    return root