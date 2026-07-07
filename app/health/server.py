from aiohttp import web
from app.config import settings

async def health_check(request):
    return web.json_response({"status": "ok"})

async def run_health_server():
    app = web.Application()
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", settings.PORT)
    await site.start()
