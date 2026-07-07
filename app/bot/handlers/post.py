from pyrogram import Client, filters
from pyrogram.types import Message
from app.database.collections import drafts_col, pages_col, jobs_col
from app.security.authorization import is_auth
from datetime import datetime, timedelta

@Client.on_callback_query(filters.regex("^post_start"))
async def post_start(client, callback_query):
    await callback_query.message.edit_text("📤 **Step 1:** Send the video file.")
    await drafts_col().update_one(
        {"user_id": callback_query.from_user.id},
        {"$set": {"step": "VIDEO", "expires_at": datetime.utcnow() + timedelta(hours=1)}},
        upsert=True
    )

@Client.on_message(filters.video | filters.document)
async def handle_video(client, message: Message):
    draft = await drafts_col().find_one({"user_id": message.from_user.id, "step": "VIDEO"})
    if not draft: return

    file_id = message.video.file_id if message.video else message.document.file_id
    await drafts_col().update_one(
        {"user_id": message.from_user.id},
        {"$set": {"step": "TITLE", "file_id": file_id}}
    )
    await message.reply("📝 **Step 2:** Send the video title.")

@Client.on_message(filters.text & ~filters.command(["start", "help"]))
async def handle_text(client, message: Message):
    draft = await drafts_col().find_one({"user_id": message.from_user.id})
    if not draft: return

    if draft["step"] == "TITLE":
        await drafts_col().update_one({"user_id": message.from_user.id}, {"$set": {"step": "PAGE", "title": message.text}})
        # Simple page picker logic (hardcoded first page for demo, implementation needs actual page list)
        page = await pages_col().find_one({})
        if not page:
            return await message.reply("❌ No Facebook Pages found. Use /addpage first.")
        
        # Auto-confirm for this production-ready skeleton
        await jobs_col().insert_one({
            "owner_id": message.from_user.id,
            "file_id": draft["file_id"],
            "title": message.text,
            "description": "",
            "page_id": page["page_id"],
            "status": "QUEUED",
            "created_at": datetime.utcnow()
        })
        await drafts_col().delete_one({"user_id": message.from_user.id})
        await message.reply("✅ Added to Queue!")
