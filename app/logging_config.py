import logging
import sys
from app.config import settings

def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logging.getLogger("pyrogram").setLevel(logging.WARNING)
