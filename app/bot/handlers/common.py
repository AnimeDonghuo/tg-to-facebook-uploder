from pyrogram import Client, filters
from app.bot.keyboards import main_markup
from app.security.authorization import is_auth

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if not await is_auth(message.from_user.id):
        return await message.reply("⛔ Access Denied.")
    
    await message.reply(
        "🎬 **TG → Facebook Uploader**\n\nDirectly publish Telegram videos to Facebook Pages.",
        reply_markup=main_markup()
    )

@Client.on_callback_query(filters.regex("^cancel_"))
async def cancel_callback(client, callback_query):
    await callback_query.answer("Action Cancelled")
    await callback_query.message.edit_text("❌ Workflow cancelled.")
