import logging
from pyrogram import Client, filters
from app.bot.keyboards import main_menu
from app.security.authorization import is_authorized

logger = logging.getLogger(__name__)

async def start_handler(client, message):
    user_id = message.from_user.id
    logger.info(f"Command /start from {user_id}")
    
    if not await is_authorized(user_id):
        return await message.reply("⛔ **Access Denied.**")
    
    await message.reply(
        "🎬 **TG → Facebook Uploader**\n\nDirectly publish Telegram videos to your Facebook Pages.",
        reply_markup=main_menu()
    )

async def help_handler(client, message):
    await message.reply("Click the buttons in /start to see specific help sections.")
