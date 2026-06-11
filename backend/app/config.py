"""Application configuration via Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "AI One"
    debug: bool = True

    # Database
    database_url: str = "postgresql+asyncpg://aione:aione@postgres:5432/aione"
    database_url_sync: str = "postgresql://aione:aione@postgres:5432/aione"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # JWT
    jwt_secret: str = "ai-one-dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Provisioning
    provision_timeout: int = 300  # seconds
    agent_image: str = "ghcr.io/nousresearch/hermes-agent:latest"

    model_config = {
        "env_file": ".env",
        "env_prefix": "AIONE_",
        "extra": "ignore",
    }


settings = Settings()
