import secrets
from typing import Any, Dict, List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "HTML Page Generator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # CORS
    ALLOWED_HOSTS: str = "http://localhost:3000,http://localhost:3001"

    # AI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # DeepSeek Configuration
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # Hugging Face Configuration
    HUGGINGFACE_API_KEY: Optional[str] = None
    HUGGINGFACE_BASE_URL: str = "https://api-inference.huggingface.co/models"
    HUGGINGFACE_MODEL: str = "deepseek-ai/DeepSeek-R1"

    # AI Provider Selection
    AI_PROVIDER: str = "huggingface"  # "openai", "deepseek", or "huggingface"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour

    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_FILE_TYPES: List[str] = ["html", "css", "js", "txt", "json"]

    # SEO
    DEFAULT_META_TITLE: str = "Generated Page"
    DEFAULT_META_DESCRIPTION: str = "AI Generated HTML Page"

    # Plugins
    PLUGINS_DIR: str = "./plugins"
    ENABLED_PLUGINS: str = "seo,analytics,social"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "app.log"

    # Monitoring
    SENTRY_DSN: Optional[str] = None
    METRICS_ENABLED: bool = True

    # Performance
    CACHE_TTL: int = 3600  # 1 hour
    MAX_WORKERS: int = 4

    # API Documentation
    DOCS_ENABLED: bool = True
    OPENAPI_DOCS_ENABLED: bool = True

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if v == "your-secret-key-here":
            # Generate secure random key for production
            return secrets.token_urlsafe(32)
        return v

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        if v.lower() in ["production", "prod"]:
            return "production"
        elif v.lower() in ["staging", "stage"]:
            return "staging"
        return "development"

    @field_validator("DEBUG")
    @classmethod
    def validate_debug(cls, v: bool) -> bool:
        # In production, debug should always be False
        return v

    @property
    def allowed_hosts_list(self) -> List[str]:
        """Parse ALLOWED_HOSTS string into list"""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]

    @property
    def enabled_plugins_list(self) -> List[str]:
        """Parse ENABLED_PLUGINS string into list"""
        return [plugin.strip() for plugin in self.ENABLED_PLUGINS.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "validate_assignment": True,
    }


settings = Settings()
