from app.database.client import get_collection

def users_col(): return get_collection("authorized_users")
def pages_col(): return get_collection("facebook_pages")
def jobs_col(): return get_collection("upload_jobs")
def drafts_col(): return get_collection("draft_sessions")
