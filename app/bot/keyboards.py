from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Single Upload", callback_data="post_start")],
        [InlineKeyboardButton("📦 Batch Mode", callback_data="batch_start")],
        [InlineKeyboardButton("📋 Queue", callback_data="view_queue"), InlineKeyboardButton("📄 Pages", callback_data="view_pages")],
        [InlineKeyboardButton("❓ Help", callback_data="help_main")]
    ])

def cancel_btn(action):
    return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{action}")]])

def back_btn(target):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=target)]])
