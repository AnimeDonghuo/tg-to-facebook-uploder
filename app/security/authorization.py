import logging
from app.database.collections import users_col
from app.config import settings

logger = logging.getLogger(__name__)

class Roles:
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    USER = "USER"

async def get_user_role(telegram_id: int) -> str | None:
    # STRIC TEST: Match owner first
    if int(telegram_id) == int(settings.OWNER_ID):
        return Roles.OWNER
    
    user = await users_col().find_one({"telegram_id": telegram_id, "enabled": True})
    return user.get("role") if user else None

async def is_authorized(telegram_id: int, min_role: str = Roles.USER) -> bool:
    role = await get_user_role(telegram_id)
    if not role:
        logger.warning(f"User {telegram_id} is not in Authorized list.")
        return False
    
    hierarchy = {Roles.USER: 1, Roles.ADMIN: 2, Roles.OWNER: 3}
    return hierarchy.get(role, 0) >= hierarchy.get(min_role, 0)
