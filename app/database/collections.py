from app.database.client import db

def users_col(): return db.db["authorized_users"]
def pages_col(): return db.db["facebook_pages"]
def jobs_col(): return db.db["upload_jobs"]
def drafts_col(): return db.db["draft_sessions"]
def batches_col(): return db.db["batches"]
def logs_col(): return db.db["sanitized_logs"]
