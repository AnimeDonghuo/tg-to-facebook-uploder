from pyrogram import Client, filters
from app.database.collections import drafts_col, jobs_col, pages_col
from datetime import datetime

@Client.on_callback_query(filters.regex("batch_start"))
async def batch_start_cb(client, cb):
    await cb.message.edit_text("📦 **Batch Mode Started**\nSend all videos, then type /done.")
    await drafts_col().update_one(
        {"user_id": cb.from_user.id},
        {"$set": {"step": "BATCH_COLLECT", "items": []}},
        upsert=True
    )

@Client.on_message(filters.command("done") & filters.private)
async def batch_done(client, message):
    draft = await drafts_col().find_one({"user_id": message.from_user.id, "step": "BATCH_COLLECT"})
    if not draft or not draft.get("items"):
        return await message.reply("No videos collected.")

    # In production, here you'd prompt for Page and then Bulk Insert
    page = await pages_col().find_one({})
    
    new_jobs = []
    for idx, item in enumerate(draft["items"]):
        new_jobs.append({
            "owner_id": message.from_user.id,
            "file_id": item,
            "title": f"Batch Upload {idx+1}", # User should use /p to rename
            "description": "",
            "page_id": page["page_id"],
            "status": "QUEUED",
            "created_at": datetime.utcnow()
        })
    
    await jobs_col().insert_many(new_jobs)
    await drafts_col().delete_one({"user_id": message.from_user.id})
    await message.reply(f"✅ {len(new_jobs)} videos added to queue!")
