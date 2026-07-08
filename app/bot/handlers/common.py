import logging
from pyrogram import Client, filters
from app.bot.keyboards import main_menu
from app.security.authorization import is_authorized

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    logger.info(f"Received /start from user: {user_id}")
    
    auth_status = await is_authorized(user_id)
    if not auth_status:
        logger.warning(f"Unauthorized access attempt by {user_id}")
        return await message.reply("⛔ **Access Denied.**\nYou are not authorized to use this bot.")
    
    await message.reply(
        "🎬 **TG → Facebook Uploader**\n\nDirectly publish Telegram videos to your Facebook Pages.",
        reply_markup=main_menu()
    )

@Client.on_message(filters.command("id") & filters.private)
async def id_handler(client, message):
    # This command always works so you can verify your ID
    await message.reply(f"Your Telegram ID is: `{message.from_user.id}`")
