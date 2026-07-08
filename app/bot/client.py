import logging
from pyrogram import Client, filters
from app.config import settings

logger = logging.getLogger(__name__)

# 1. Manual Diagnostic Handler (to prove connectivity)
# This will run even if the plugin loader fails
async def diagnostic_handler(client, message):
    logger.info(f"DIAGNOSTIC: Received message from {message.from_user.id}")
    if message.text == "/ping":
        await message.reply("Pong! The bot is receiving messages.")

bot = Client(
    "tg_fb_uploader",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    # Try the absolute module path for plugins
    plugins=dict(root="app.bot.handlers")
)

# Register the diagnostic handler manually
bot.add_handler(filters.command("ping") & filters.private, diagnostic_handler)
