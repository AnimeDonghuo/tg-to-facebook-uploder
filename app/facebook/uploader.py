import os
import aiohttp
import logging
from app.config import settings
from app.facebook.errors import classify_fb_error

logger = logging.getLogger(__name__)

class FacebookUploader:
    def __init__(self, token: str, page_id: str):
        self.token = token
        self.page_id = page_id
        self.url = f"https://graph.facebook.com/{settings.GRAPH_API_VERSION}/{page_id}/videos"

    async def upload(self, file_path: str, title: str, description: str, progress_cb=None):
        file_size = os.path.getsize(file_path)
        
        async with aiohttp.ClientSession() as session:
            # 1. Start Phase
            async with session.post(self.url, params={
                "upload_phase": "start",
                "file_size": file_size,
                "access_token": self.token
            }) as r:
                data = await r.json()
                if r.status != 200: raise classify_fb_error(data)
                session_id = data["upload_session_id"]

            # 2. Transfer Phase (Chunked)
            chunk_size = 4 * 1024 * 1024 # 4MB
            offset = 0
            with open(file_path, "rb") as f:
                while offset < file_size:
                    chunk = f.read(chunk_size)
                    form = aiohttp.FormData()
                    form.add_field("video_file_chunk", chunk, filename="blob")
                    
                    async with session.post(self.url, params={
                        "upload_phase": "transfer",
                        "upload_session_id": session_id,
                        "start_offset": offset,
                        "access_token": self.token
                    }, data=form) as r:
                        res = await r.json()
                        if r.status != 200: raise classify_fb_error(res)
                    
                    offset += len(chunk)
                    if progress_cb:
                        await progress_cb(offset, file_size)

            # 3. Finish Phase
            async with session.post(self.url, params={
                "upload_phase": "finish",
                "upload_session_id": session_id,
                "title": title,
                "description": description,
                "access_token": self.token
            }) as r:
                final = await r.json()
                if r.status != 200: raise classify_fb_error(final)
                return final
