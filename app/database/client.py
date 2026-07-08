from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DATABASE]
        await self.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB.")

    async def close(self):
        if self.client:
            self.client.close()

db = MongoDB()
