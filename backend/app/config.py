"""Application configuration via Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    ***REMOVED*** Application
    app_name: str = "AI One"
    debug: bool = True

    ***REMOVED*** Database
    database_url: str = "postgresql+asyncpg://REDACTED:REDACTED@postgres:5432/aione"
    database_url_sync: str = "postgresql://REDACTED:REDACTED@postgres:5432/aione"

    ***REMOVED*** Redis
    redis_url: str = "redis://redis:6379/0"

    ***REMOVED*** JWT
    jwt_secret: str = "ai-one-dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"

    ***REMOVED*** CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    ***REMOVED*** Provisioning
    provision_timeout: int = 300  ***REMOVED*** seconds
    agent_image: str = "ghcr.io/nousresearch/hermes-agent:latest"

    model_config = {
        "env_file": ".env",
        "env_prefix": "AIONE_",
        "extra": "ignore",
    }


settings = Settings()
