from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Upload Video", callback_data="post_start")],
        [InlineKeyboardButton("📦 Batch Upload", callback_data="batch_start")],
        [InlineKeyboardButton("📋 Queue", callback_data="view_queue"), InlineKeyboardButton("📄 Pages", callback_data="view_pages")]
    ])

def cancel_markup(action: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{action}")]])
