import asyncio
import os
import logging
from datetime import datetime
from app.database.collections import jobs_col, pages_col
from app.security.token_cipher import cipher
from app.facebook.uploader import FacebookUploader
from app.bot.client import bot
from app.utils.files import cleanup_temp, ensure_temp, get_free_disk_mb
from app.config import settings
from app.bot.progress import ProgressHandler

logger = logging.getLogger(__name__)

async def run_worker():
    ensure_temp()
    logger.info("Upload Worker Initialized.")
    
    while True:
        # Find next queued job
        job = await jobs_col().find_one_and_update(
            {"status": "QUEUED"},
            {"$set": {"status": "CLAIMED", "locked_at": datetime.utcnow()}},
            sort=[("created_at", 1)]
        )
        
        if not job:
            await asyncio.sleep(10)
            continue

        try:
            await process_job(job)
        except Exception as e:
            logger.error(f"Worker Error on Job {job['_id']}: {e}")
            await jobs_col().update_one(
                {"_id": job["_id"]}, 
                {"$set": {"status": "FAILED", "error": str(e)}}
            )

async def process_job(job):
    job_id = str(job["_id"])
    
    # 1. Check Disk
    if get_free_disk_mb() < settings.MIN_FREE_DISK_MB:
        raise Exception("Insufficient disk space on server.")

    # 2. Page & Token
    page = await pages_col().find_one({"page_id": job["page_id"]})
    if not page: raise Exception("Target Facebook Page not found.")
    token = cipher.decrypt(page["encrypted_token"])

    # 3. Download
    await jobs_col().update_one({"_id": job["_id"]}, {"$set": {"status": "DOWNLOADING"}})
    
    # Notify user (if available)
    status_msg = await bot.send_message(job["owner_id"], f"⏳ Processing Job: `{job_id}`")
    progress = ProgressHandler(status_msg, "Downloading from Telegram")
    
    local_path = await bot.download_media(
        job["file_id"], 
        file_name=f"{settings.TEMP_DIR}/{job_id}.mp4",
        progress=progress.update
    )

    # 4. Upload
    await jobs_col().update_one({"_id": job["_id"]}, {"$set": {"status": "UPLOADING"}})
    progress.stage = "Uploading to Facebook"
    
    uploader = FacebookUploader(token, job["page_id"])
    result = await uploader.upload(
        local_path, 
        job["title"], 
        job["description"], 
        progress_cb=progress.update
    )

    # 5. Success
    cleanup_temp(local_path)
    await jobs_col().update_one({"_id": job["_id"]}, {
        "$set": {"status": "COMPLETED", "fb_id": result.get("id"), "finished_at": datetime.utcnow()}
    })
    await status_msg.edit_text(f"✅ **Published Successfully!**\n\nTitle: {job['title']}\nFB Video ID: `{result.get('id')}`")
