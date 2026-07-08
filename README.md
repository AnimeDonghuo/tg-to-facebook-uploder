# TG-Facebook-Uploader

A professional-grade, private Telegram bot to bridge Telegram media and Facebook Page video publishing. Optimized for deployment on Koyeb's ephemeral infrastructure.

## 🚀 Key Features
- **MTProto Powered**: Uses Pyrogram for high-performance Telegram interaction.
- **Official Meta API**: Uses chunked, resumable uploads for large video files.
- **Persistent Queue**: Jobs are stored in MongoDB to survive application restarts.
- **Batch Processing**: Advanced batch collection mode with sequential title assignment.
- **RBAC Security**: Owner, Admin, and User roles with strict permission checks.
- **Encrypted Secrets**: Facebook Page tokens are AES-256 encrypted at rest.
- **Resource Optimized**: Low RAM/Disk usage with sequential processing.

## 🛠 Setup & Deployment

### 1. Requirements
- Python 3.11+
- MongoDB (Atlas recommended)
- Telegram `API_ID`, `API_HASH`, and `BOT_TOKEN`
- Meta App with `pages_manage_posts` and `page_video_reels_publishing` permissions.

### 2. Encryption Key
Generate a `TOKEN_ENCRYPTION_KEY`:
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
