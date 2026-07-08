from pyrogram import Client, filters
from app.database.collections import drafts_col, jobs_col, pages_col
from datetime import datetime, timedelta

@Client.on_message(filters.command("batch") & filters.private)
async def batch_start_cmd(client, message):
    await drafts_col().update_one(
        {"user_id": message.from_user.id},
        {"$set": {"step": "BATCH_COLLECT", "items": [], "expires_at": datetime.utcnow() + timedelta(hours=24)}},
        upsert=True
    )
    await message.reply("📦 **Batch Mode Started**\n\nSend multiple videos. When finished, send /done.")

@Client.on_message(filters.command("done") & filters.private)
async def batch_done_cmd(client, message):
    draft = await drafts_col().find_one({"user_id": message.from_user.id, "step": "BATCH_COLLECT"})
    if not draft or not draft.get("items"):
        return await message.reply("❌ No videos collected in batch.")

    page = await pages_col().find_one({}) # Default to first page
    if not page:
        return await message.reply("❌ No Facebook Page linked. Use /addpage.")

    for idx, file_id in enumerate(draft["items"]):
        await jobs_col().insert_one({
            "owner_id": message.from_user.id,
            "file_id": file_id,
            "title": f"Video {idx + 1}",
            "description": "",
            "page_id": page["page_id"],
            "status": "QUEUED",
            "created_at": datetime.utcnow()
        })

    await drafts_col().delete_one({"user_id": message.from_user.id})
    await message.reply(f"✅ Batch processed. {len(draft['items'])} videos added to /queue.")
