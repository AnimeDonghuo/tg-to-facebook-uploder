import asyncio
import uvloop
import sys
import os
import logging

# Ensure the root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.bot.client import bot
from app.database.client import db
from app.database.indexes import create_indexes
from app.logging_config import setup_logging
from app.queue.worker import run_worker
from app.health.server import start_health_server

logger = logging.getLogger("app.main")

async def main():
    setup_logging()
    
    try:
        # 1. Database
        await db.connect()
        await create_indexes()
        
        # 2. Start Health Server (Koyeb needs this to pass health checks)
        asyncio.create_task(start_health_server())
        
        # 3. Start Worker
        asyncio.create_task(run_worker())
        
        # 4. Start Bot
        logger.info("Starting Pyrogram Client...")
        await bot.start()
        
        # Log the bot's username to verify it's the right one
        me = await bot.get_me()
        logger.info(f"Bot started as @{me.username}")
        
        # Keep alive
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Critical error during startup: {e}", exc_info=True)
    finally:
        await bot.stop()
        await db.close()

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
