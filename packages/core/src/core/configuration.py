from pydantic_settings import BaseSettings, SettingsConfigDict

from core.secures import KeyBackend


class Configuration(BaseSettings):
    # app - [DEVELOPMENT, PRODUCTION]
    MODE: str
    CRYPTO_BACKEND: str = KeyBackend.EC.value
    CORS_ALLOWED_ORIGINS: str
    MAX_AGE: int = 3600

    # database
    LOCAL_URI: str
    REMOTE_URI: str
    IS_LOCAL: bool
    IS_SYNC_DATABASE_ENABLED: bool
    SYNC_DATABASE_INTERVAL: int

    # roboflow
    ROBOFLOW_KEY: str

    # supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_PASSWORD: str

    # cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # queue
    RABBITMQ_BROKER_URL: str

    # google
    GEMINI_API_KEY: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")
