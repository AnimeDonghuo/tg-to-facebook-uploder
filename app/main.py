import asyncio
import uvloop
import sys
import os
import logging

# Ensure root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.bot.client import bot, register_all_handlers
from app.database.client import db
from app.database.indexes import create_indexes
from app.logging_config import setup_logging
from app.queue.worker import run_worker
from app.health.server import start_health_server

logger = logging.getLogger("app.main")

async def main():
    setup_logging()
    
    try:
        await db.connect()
        await create_indexes()
        
        # 1. Register handlers MANUALLY
        register_all_handlers()
        
        # 2. Background tasks
        asyncio.create_task(start_health_server())
        asyncio.create_task(run_worker())
        
        # 3. Start Bot
        logger.info("Starting Pyrogram Client...")
        await bot.start()
        
        me = await bot.get_me()
        logger.info(f"Bot started successfully as @{me.username}")
        
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Startup failed: {e}", exc_info=True)
    finally:
        await bot.stop()
        await db.close()

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
