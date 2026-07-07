import aiohttp
from app.config import settings

class MetaAPI:
    def __init__(self):
        self.base_url = f"https://graph.facebook.com/{settings.GRAPH_API_VERSION}"

    async def get_page(self, token: str, page_id: str = "me"):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{page_id}"
            params = {"access_token": token, "fields": "id,name,access_token"}
            async with session.get(url, params=params) as r:
                return await r.json()

meta_api = MetaAPI()
