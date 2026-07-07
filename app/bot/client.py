from pyrogram import Client
from app.config import settings

bot = Client(
    "tg_fb_bot",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    plugins=dict(root="app/bot/handlers")
)
