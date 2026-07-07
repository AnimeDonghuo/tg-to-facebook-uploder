from pyrogram import Client, filters
from app.security.authorization import is_auth, Roles
from app.facebook.client import meta_api
from app.security.token_cipher import cipher
from app.database.collections import pages_col

@Client.on_message(filters.command("addpage") & filters.private)
async def add_page_cmd(client, message):
    if not await is_auth(message.from_user.id, Roles.OWNER):
        return await message.reply("⛔ Admin only.")
    
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Usage: `/addpage {token}`")
    
    token = parts[1]
    try:
        data = await meta_api.get_page(token)
        if "id" not in data: raise Exception(str(data))
        
        encrypted = cipher.encrypt(token)
        await pages_col().update_one(
            {"page_id": data["id"]},
            {"$set": {"name": data["name"], "encrypted_token": encrypted}},
            upsert=True
        )
        await message.reply(f"✅ Page Linked: **{data['name']}**")
        await message.delete() # Security: delete token message
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
