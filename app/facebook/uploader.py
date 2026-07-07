import os
import aiohttp
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class FacebookUploader:
    def __init__(self, token: str, page_id: str):
        self.token = token
        self.page_id = page_id
        self.url = f"https://graph.facebook.com/{settings.GRAPH_API_VERSION}/{page_id}/videos"

    async def upload(self, path: str, title: str, desc: str, progress_cb=None):
        size = os.path.getsize(path)
        
        # 1. Start
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, params={
                "upload_phase": "start", "file_size": size, "access_token": self.token
            }) as r:
                data = await r.json()
                if "upload_session_id" not in data: raise Exception(f"FB Start Error: {data}")
                sid = data["upload_session_id"]

            # 2. Transfer
            chunk_size = 4 * 1024 * 1024
            offset = 0
            with open(path, "rb") as f:
                while offset < size:
                    chunk = f.read(chunk_size)
                    form = aiohttp.FormData()
                    form.add_field("video_file_chunk", chunk)
                    async with session.post(self.url, params={
                        "upload_phase": "transfer", "upload_session_id": sid,
                        "start_offset": offset, "access_token": self.token
                    }, data=form) as r:
                        if r.status != 200: raise Exception(await r.text())
                    offset += len(chunk)
                    if progress_cb: await progress_cb(offset, size)

            # 3. Finish
            async with session.post(self.url, params={
                "upload_phase": "finish", "upload_session_id": sid,
                "title": title, "description": desc, "access_token": self.token
            }) as r:
                return await r.json()
