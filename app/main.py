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
        # 1. Connect to Database
        await db.connect()
        await create_indexes()
        
        # 2. Register Telegram Handlers
        register_all_handlers()
        
        # 3. Start Background tasks
        asyncio.create_task(start_health_server())
        asyncio.create_task(run_worker())
        
        # 4. Start Bot
        logger.info("Starting Pyrogram Client...")
        await bot.start()
        
        me = await bot.get_me()
        logger.info(f"🚀 Bot is online as @{me.username}")
        
        # Wait until the process is stopped
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
    finally:
        # Safe shutdown
        if bot.is_connected:
            await bot.stop()
        await db.close()

if __name__ == "__main__":
    if sys.platform != 'win32':
        uvloop.install()
    asyncio.run(main())
