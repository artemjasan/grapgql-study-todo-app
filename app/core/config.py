import secrets


class Settings:
    POSTGRES_URI: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    # Secrets
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"


settings = Settings()
