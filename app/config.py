from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    API_ID: int
    API_HASH: str
    BOT_TOKEN: str
    OWNER_ID: int

    MONGODB_URL: str
    MONGODB_DATABASE: str = "tg_fb_uploader"

    TOKEN_ENCRYPTION_KEY: str

    GRAPH_API_VERSION: str = "v19.0"
    PORT: int = 8000

    TEMP_DIR: str = "/tmp/tgfb"
    MIN_FREE_DISK_MB: int = 512
    MAX_TEMP_FILE_AGE_HOURS: int = 24

    WORKER_CONCURRENCY: int = 1
    JOB_LEASE_SECONDS: int = 600
    JOB_HEARTBEAT_SECONDS: int = 30

    MAX_RETRIES: int = 5
    RETRY_BASE_DELAY: int = 60
    RETRY_MAX_DELAY: int = 3600

    PROGRESS_UPDATE_SECONDS: int = 7
    TIMEZONE: str = "UTC"
    LOG_LEVEL: str = "INFO"

    HISTORY_RETENTION_DAYS: int = 30
    LOG_RETENTION_DAYS: int = 7
    DRAFT_TTL_HOURS: int = 24

    ALLOW_ADMIN_PAGE_MANAGEMENT: bool = False

settings = Settings()
