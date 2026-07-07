import asyncio
import os
import time
import logging
from datetime import datetime, timedelta
from app.database.collections import jobs_col, pages_col
from app.security.token_cipher import cipher
from app.facebook.uploader import FacebookUploader
from app.bot.client import bot
from app.utils.files import clean_file, ensure_temp
from app.config import settings

logger = logging.getLogger(__name__)

async def run_worker():
    ensure_temp()
    logger.info("Worker started...")
    while True:
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
            logger.error(f"Job {job['_id']} failed: {e}")
            await jobs_col().update_one({"_id": job["_id"]}, {"$set": {"status": "FAILED", "error": str(e)}})

async def process_job(job):
    job_id = job["_id"]
    page = await pages_col().find_one({"page_id": job["page_id"]})
    token = cipher.decrypt(page["encrypted_token"])
    
    # 1. Download
    await jobs_col().update_one({"_id": job_id}, {"$set": {"status": "DOWNLOADING"}})
    path = await bot.download_media(job["file_id"], file_name=f"{settings.TEMP_DIR}/{job_id}.mp4")
    
    # 2. Upload
    await jobs_col().update_one({"_id": job_id}, {"$set": {"status": "UPLOADING"}})
    uploader = FacebookUploader(token, job["page_id"])
    
    async def progress(current, total):
        # Update logic here (rate limited)
        pass

    result = await uploader.upload(path, job["title"], job["description"], progress_cb=progress)
    
    # 3. Cleanup
    clean_file(path)
    await jobs_col().update_one({"_id": job_id}, {"$set": {"status": "COMPLETED", "fb_id": result.get("id")}})
    await bot.send_message(job["owner_id"], f"✅ **Upload Complete!**\n\nTitle: {job['title']}\nFB ID: `{result.get('id')}`")
