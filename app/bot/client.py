import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from app.config import settings

logger = logging.getLogger(__name__)

# Create the client without the automatic plugin loader
bot = Client(
    "tg_fb_uploader",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN
)

def register_all_handlers():
    """
    Manually register handlers using the correct Pyrogram Handler classes.
    """
    from app.bot.handlers.common import start_handler, help_handler
    from app.bot.handlers.pages import add_page_handler
    from app.bot.handlers.post import post_cb, video_receiver, text_receiver
    from app.bot.handlers.batch import batch_start_cmd, batch_done_cmd

    # 1. Common Commands
    bot.add_handler(MessageHandler(start_handler, filters.command("start") & filters.private))
    bot.add_handler(MessageHandler(help_handler, filters.command("help") & filters.private))

    # 2. Page Management
    bot.add_handler(MessageHandler(add_page_handler, filters.command("addpage") & filters.private))

    # 3. Upload Workflow (Callback Queries)
    bot.add_handler(CallbackQueryHandler(post_cb, filters.regex("post_start")))
    bot.add_handler(CallbackQueryHandler(batch_start_cmd, filters.regex("batch_start")))

    # 4. Media Receivers
    bot.add_handler(MessageHandler(video_receiver, (filters.video | filters.document) & filters.private))
    
    # 5. Text / Title Receiver (Exclude commands)
    text_filter = filters.text & filters.private & ~filters.command(["start", "help", "cancel", "addpage", "batch", "done"])
    bot.add_handler(MessageHandler(text_receiver, text_filter))

    # 6. Batch Commands
    bot.add_handler(MessageHandler(batch_start_cmd, filters.command("batch") & filters.private))
    bot.add_handler(MessageHandler(batch_done_cmd, filters.command("done") & filters.private))

    logger.info("✅ All Telegram handlers registered manually via Handler Classes.")
