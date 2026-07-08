import asyncio
import uvloop
import sys
import os

# Add the current directory to sys.path to prevent import errors in different environments
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.bot.client import bot
from app.database.client import db
from app.database.indexes import create_indexes
from app.logging_config import setup_logging
from app.queue.worker import run_worker
from app.health.server import start_health_server

async def main():
    setup_logging()
    
    # 1. Initialize Database
    try:
        await db.connect()
        await create_indexes()
    except Exception as e:
        print(f"CRITICAL: Database connection failed: {e}")
        return

    # 2. Start Background Tasks
    asyncio.create_task(start_health_server())
    asyncio.create_task(run_worker())
    
    # 3. Start Telegram Bot
    print("Bot is starting...")
    try:
        await bot.start()
        print("Bot started. Press Ctrl+C to stop.")
        # Keep the bot running
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopping...")
    finally:
        await bot.stop()
        await db.close()

if __name__ == "__main__":
    # Use uvloop for better performance on Linux (Koyeb)
    if sys.platform != 'win32':
        uvloop.install()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
