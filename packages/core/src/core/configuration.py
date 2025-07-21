from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    # app - [DEVELOPMENT, PRODUCTION]
    MODE: str

    # database
    URI: str

    # roboflow
    ROBOFLOW_KEY: str

    # supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_PASSWORD: str

    # cors
    CORS_ALLOWED_ORIGINS: str
    MAX_AGE: int = 3600

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")


config = Configuration()
