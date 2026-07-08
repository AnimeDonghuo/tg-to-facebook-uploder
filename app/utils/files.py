import os
import shutil
from app.config import settings

def ensure_temp():
    if not os.path.exists(settings.TEMP_DIR):
        os.makedirs(settings.TEMP_DIR)

def get_free_disk_mb():
    stat = shutil.disk_usage(settings.TEMP_DIR)
    return stat.free // (1024 * 1024)

def cleanup_temp(file_path: str):
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
