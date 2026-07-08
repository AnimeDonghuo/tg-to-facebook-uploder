from app.database.collections import users_col
from app.config import settings

class Roles:
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    USER = "USER"

async def get_user_role(telegram_id: int) -> str | None:
    if telegram_id == settings.OWNER_ID:
        return Roles.OWNER
    user = await users_col().find_one({"telegram_id": telegram_id, "enabled": True})
    return user.get("role") if user else None

async def is_authorized(telegram_id: int, min_role: str = Roles.USER) -> bool:
    role = await get_user_role(telegram_id)
    if not role: return False
    hierarchy = {Roles.USER: 1, Roles.ADMIN: 2, Roles.OWNER: 3}
    return hierarchy.get(role, 0) >= hierarchy.get(min_role, 0)
