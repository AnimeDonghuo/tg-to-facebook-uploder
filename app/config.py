from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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
    
    WORKER_CONCURRENCY: int = 1
    JOB_LEASE_SECONDS: int = 600
    PROGRESS_UPDATE_SECONDS: int = 5
    LOG_LEVEL: str = "INFO"

settings = Settings()
