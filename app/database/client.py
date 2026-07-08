from motor.motor_asyncio import AsyncIOMotorClient
import pymongo # Added to ensure it's loaded
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            # We explicitly use the stable motor client
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client[settings.MONGODB_DATABASE]
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    async def close(self):
        if self.client:
            self.client.close()

db = MongoDB()
