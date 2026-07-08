from pyrogram import Client, filters
from app.database.collections import drafts_col, pages_col, jobs_col
from app.bot.keyboards import cancel_btn
from datetime import datetime, timedelta

@Client.on_callback_query(filters.regex("post_start"))
async def post_cb(client, cb):
    await cb.message.edit_text("📤 Send me the video you want to upload.", reply_markup=cancel_btn("post"))
    await drafts_col().update_one(
        {"user_id": cb.from_user.id},
        {"$set": {"step": "VIDEO", "expires_at": datetime.utcnow() + timedelta(hours=1)}},
        upsert=True
    )

@Client.on_message(filters.video | filters.document)
async def video_receiver(client, message):
    draft = await drafts_col().find_one({"user_id": message.from_user.id, "step": "VIDEO"})
    if not draft: return

    file_id = message.video.file_id if message.video else message.document.file_id
    await drafts_col().update_one({"user_id": message.from_user.id}, {"$set": {"step": "TITLE", "file_id": file_id}})
    await message.reply("📝 Now send the **Title** for this video.")

@Client.on_message(filters.text & ~filters.command(["start", "help", "cancel"]))
async def text_receiver(client, message):
    draft = await drafts_col().find_one({"user_id": message.from_user.id})
    if not draft: return

    if draft["step"] == "TITLE":
        # Simplified: Auto-assign first page for MVP clarity, in production show picker
        page = await pages_col().find_one({})
        if not page:
            return await message.reply("❌ No Facebook Page configured. Add one with /addpage.")

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
        await message.reply("✅ Job added to queue! Use /queue to track.")
