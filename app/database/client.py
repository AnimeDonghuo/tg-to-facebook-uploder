from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DATABASE]
        await self.client.admin.command('ping')

    async def close(self):
        if self.client:
            self.client.close()

db = MongoDB()

def get_collection(name: str):
    return db.db[name]
