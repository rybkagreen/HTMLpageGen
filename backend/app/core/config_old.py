from typing import List, Optional

from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "HTML Page Generator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./app.db")

    # Redis
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379")

    # CORS
    ALLOWED_HOSTS: List[str] = config(
        "ALLOWED_HOSTS",
        default="http://localhost:3000,http://localhost:3001",
        cast=lambda v: [s.strip() for s in v.split(",")],
    )

    # AI Configuration
    OPENAI_API_KEY: Optional[str] = config("OPENAI_API_KEY", default=None)
    OPENAI_MODEL: str = config("OPENAI_MODEL", default="gpt-3.5-turbo")

    # DeepSeek Configuration
    DEEPSEEK_API_KEY: Optional[str] = config("DEEPSEEK_API_KEY", default=None)
    DEEPSEEK_BASE_URL: str = config(
        "DEEPSEEK_BASE_URL", default="https://api.deepseek.com/v1"
    )
    DEEPSEEK_MODEL: str = config("DEEPSEEK_MODEL", default="deepseek-chat")

    # AI Provider Selection
    AI_PROVIDER: str = config("AI_PROVIDER", default="openai")  # "openai" or "deepseek"

    # Security
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int
    )

    # File Upload
    MAX_FILE_SIZE: int = config("MAX_FILE_SIZE", default=10485760, cast=int)  # 10MB
    UPLOAD_DIR: str = config("UPLOAD_DIR", default="./uploads")

    # SEO
    DEFAULT_META_TITLE: str = config("DEFAULT_META_TITLE", default="Generated Page")
    DEFAULT_META_DESCRIPTION: str = config(
        "DEFAULT_META_DESCRIPTION", default="AI Generated HTML Page"
    )

    # Plugins
    PLUGINS_DIR: str = config("PLUGINS_DIR", default="./plugins")
    ENABLED_PLUGINS: List[str] = config(
        "ENABLED_PLUGINS",
        default="seo,analytics,social",
        cast=lambda v: [s.strip() for s in v.split(",")],
    )

    class Config:
        env_file = ".env"


settings = Settings()
