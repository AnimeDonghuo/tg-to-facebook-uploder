from app.database.collections import users_col
from app.config import settings

class Roles:
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    USER = "USER"

async def get_user_role(user_id: int):
    if user_id == settings.OWNER_ID:
        return Roles.OWNER
    user = await users_col().find_one({"telegram_id": user_id, "enabled": True})
    return user.get("role") if user else None

async def is_auth(user_id: int, min_role=Roles.USER):
    role = await get_user_role(user_id)
    if not role: return False
    hierarchy = {Roles.USER: 1, Roles.ADMIN: 2, Roles.OWNER: 3}
    return hierarchy.get(role, 0) >= hierarchy.get(min_role, 0)
