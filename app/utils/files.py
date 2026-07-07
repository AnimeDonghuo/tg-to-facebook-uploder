import os
import shutil
from app.config import settings

def ensure_temp():
    if not os.path.exists(settings.TEMP_DIR):
        os.makedirs(settings.TEMP_DIR)

def get_free_space_mb():
    stat = shutil.disk_usage(settings.TEMP_DIR)
    return stat.free // (1024 * 1024)

def clean_file(path: str):
    if path and os.path.exists(path):
        os.remove(path)
