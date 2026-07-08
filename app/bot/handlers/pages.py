from pyrogram import Client, filters
from app.security.authorization import is_authorized, Roles
from app.facebook.client import fb_api
from app.security.token_cipher import cipher
from app.database.collections import pages_col
from app.config import settings

@Client.on_message(filters.command("addpage") & filters.private)
async def add_page_handler(client, message):
    if not await is_authorized(message.from_user.id, Roles.OWNER):
        return await message.reply("⛔ Unauthorized.")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: `/addpage {token}`")

    token = parts[1]
    try:
        details = await fb_api.get_page_details(token)
        enc_token = cipher.encrypt(token)
        
        await pages_col().update_one(
            {"page_id": details["id"]},
            {"$set": {"name": details["name"], "encrypted_token": enc_token}},
            upsert=True
        )
        await message.reply(f"✅ Linked Page: **{details['name']}** (`{details['id']}`)")
        await message.delete() # Security
    except Exception as e:
        await message.reply(f"❌ Failed to add page: {e}")
