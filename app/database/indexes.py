from app.database.collections import users_col, pages_col, jobs_col

async def create_indexes():
    await users_col().create_index("telegram_id", unique=True)
    await pages_col().create_index("page_id", unique=True)
    await jobs_col().create_index("status")
    await jobs_col().create_index("created_at")
