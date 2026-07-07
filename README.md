# TG-Facebook-Uploader

A professional-grade, private Telegram bot designed to bridge Telegram media and Facebook Page video publishing. Optimized for deployment on Koyeb's ephemeral infrastructure with low RAM and disk footprints.

## 🚀 Features
- **Large Video Support**: Handles files up to 4GB (Telegram limit) and uploads via Meta's resumable chunked API.
- **Persistent Queue**: All jobs are stored in MongoDB, ensuring recovery after application restarts.
- **Batch Uploading**: Collect multiple videos and assign titles/descriptions in one workflow.
- **Role-Based Access Control**: OWNER, ADMIN, and USER levels.
- **Secure Token Storage**: Facebook Page tokens are encrypted at rest using AES-256 (Fernet).
- **Sequential Worker**: Processes uploads one at a time to stay within Koyeb's free-tier limits.
- **Real-time Progress**: Live Telegram updates for download and upload stages.

## 🛠 Tech Stack
- Python 3.11, Pyrogram, Motor (MongoDB), Cryptography, aiohttp, Docker.

## 📋 Quick Start
1. Clone the repo.
2. Create a `.env` file based on `.env.example`.
3. Generate an encryption key: `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
4. Run `docker-compose up --build`.
