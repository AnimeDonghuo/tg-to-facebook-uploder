import logging
from pyrogram import Client, filters
from app.config import settings

logger = logging.getLogger(__name__)

# Create the client WITHOUT the plugin loader to avoid path errors
bot = Client(
    "tg_fb_uploader",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN
)

def register_all_handlers():
    """
    Manually import and register handlers to guarantee they are loaded.
    """
    from app.bot.handlers.common import start_handler, help_handler
    from app.bot.handlers.pages import add_page_handler
    from app.bot.handlers.post import post_cb, video_receiver, text_receiver
    from app.bot.handlers.batch import batch_start_cmd, batch_done_cmd

    # Common
    bot.add_handler(filters.command("start") & filters.private, start_handler)
    bot.add_handler(filters.command("help") & filters.private, help_handler)

    # Pages
    bot.add_handler(filters.command("addpage") & filters.private, add_page_handler)

    # Post Workflow
    bot.add_handler(filters.callback_query(filters.regex("post_start")), post_cb)
    bot.add_handler((filters.video | filters.document) & filters.private, video_receiver)
    # This filter ensures we don't catch commands as titles
    bot.add_handler(filters.text & filters.private & ~filters.command(["start", "help", "cancel", "addpage", "batch", "done"]), text_receiver)

    # Batch Workflow
    bot.add_handler(filters.callback_query(filters.regex("batch_start")), batch_start_cmd) # reused command as logic
    bot.add_handler(filters.command("batch") & filters.private, batch_start_cmd)
    bot.add_handler(filters.command("done") & filters.private, batch_done_cmd)

    logger.info("All Telegram handlers registered manually.")
