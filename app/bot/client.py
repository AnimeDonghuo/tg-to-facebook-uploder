from pyrogram import Client
from app.config import settings

# Using the full module path "app.bot.handlers" is more reliable for Docker
bot = Client(
    "tg_fb_uploader",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    plugins=dict(root="app.bot.handlers") 
)
