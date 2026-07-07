import asyncio
from app.bot.client import bot
from app.database.client import db
from app.database.indexes import create_indexes
from app.logging_config import setup_logging
from app.queue.worker import run_worker
from app.health.server import run_health_server

async def main():
    setup_logging()
    await db.connect()
    await create_indexes()
    
    # Start background tasks
    asyncio.create_task(run_health_server())
    asyncio.create_task(run_worker())
    
    print("Bot is starting...")
    await bot.start()
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
