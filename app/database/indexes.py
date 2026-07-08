from app.database.collections import users_col, pages_col, jobs_col, drafts_col

async def create_indexes():
    await users_col().create_index("telegram_id", unique=True)
    await pages_col().create_index("page_id", unique=True)
    await jobs_col().create_index([("status", 1), ("created_at", 1)])
    await jobs_col().create_index("retry_at")
    await drafts_col().create_index("expires_at", expireAfterSeconds=0)
