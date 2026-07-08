import asyncio
import uvloop
from app.bot.client import bot
from app.database.client import db
from app.database.indexes import create_indexes
from app.logging_config import setup_logging
from app.queue.worker import run_worker
from app.health.server import start_health_server

async def main():
    setup_logging()
    
    # Init DB
    await db.connect()
    await create_indexes()
    
    # Start Health Server & Worker
    asyncio.create_task(start_health_server())
    asyncio.create_task(run_worker())
    
    # Start Bot
    print("Bot is starting...")
    await bot.start()
    
    # Idle
    await asyncio.Event().wait()

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main())
