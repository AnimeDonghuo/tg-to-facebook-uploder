from app.database.collections import users_col, pages_col, jobs_col, drafts_col

async def create_indexes():
    # User Indexes
    await users_col().create_index("telegram_id", unique=True)
    
    # Page Indexes
    await pages_col().create_index("page_id", unique=True)
    
    # Job Indexes
    await jobs_col().create_index([("status", 1), ("created_at", 1)])
    await jobs_col().create_index("owner_id")
    await jobs_col().create_index("retry_at")
    
    # TTL Index for Drafts (Automatic cleanup after 24 hours)
    await drafts_col().create_index("expires_at", expireAfterSeconds=0)
    
    print("Database indexes synchronized.")
