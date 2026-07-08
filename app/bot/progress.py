import time
import humanize
from app.config import settings

class ProgressHandler:
    def __init__(self, message, stage_name):
        self.message = message
        self.stage = stage_name
        self.last_update = 0

    async def update(self, current, total):
        now = time.time()
        if now - self.last_update < settings.PROGRESS_UPDATE_SECONDS:
            return

        percentage = (current / total) * 100
        cur_h = humanize.naturalsize(current)
        tot_h = humanize.naturalsize(total)
        
        text = (
            f"⚙️ **Stage:** {self.stage}\n"
            f"📊 **Progress:** {percentage:.1f}%\n"
            f"📦 **Size:** {cur_h} / {tot_h}"
        )
        
        try:
            await self.message.edit_text(text)
            self.last_update = now
        except:
            pass
