import aiohttp
from app.config import settings
from app.facebook.errors import classify_fb_error

class MetaGraphClient:
    def __init__(self):
        self.base_url = f"https://graph.facebook.com/{settings.GRAPH_API_VERSION}"

    async def request(self, method, endpoint, token, params=None, data=None):
        if params is None: params = {}
        params["access_token"] = token
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.base_url}/{endpoint}", params=params, json=data) as r:
                res = await r.json()
                if r.status != 200:
                    raise classify_fb_error(res)
                return res

    async def get_page_details(self, token: str):
        # Validates token and gets ID/Name
        return await self.request("GET", "me", token, params={"fields": "id,name"})

fb_api = MetaGraphClient()
