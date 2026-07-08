from pyrogram import Client, filters
from app.bot.keyboards import main_menu
from app.security.authorization import is_authorized

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if not await is_authorized(message.from_user.id):
        return await message.reply("⛔ Access Denied.")
    
    await message.reply(
        "🎬 **TG → Facebook Uploader**\n\nDirectly publish Telegram videos to your Facebook Pages.",
        reply_markup=main_menu()
    )

@Client.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    await message.reply("Use the /start menu to navigate or see detailed help via buttons.")

@Client.on_callback_query(filters.regex("^cancel_"))
async def cancel_callback(client, cb):
    await cb.message.edit_text("❌ Action Cancelled.")
