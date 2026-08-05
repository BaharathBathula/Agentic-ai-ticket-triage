import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "Agentic AI Ticket Triage",
    )
    app_version: str = os.getenv(
        "APP_VERSION",
        "1.1.0",
    )
    environment: str = os.getenv(
        "APP_ENV",
        "development",
    )
    host: str = os.getenv(
        "APP_HOST",
        "0.0.0.0",
    )
    port: int = int(
        os.getenv(
            "APP_PORT",
            "8000",
        )
    )
    database_path: str | None = os.getenv(
        "DATABASE_PATH",
    )
    openai_api_key: str | None = os.getenv(
        "OPENAI_API_KEY",
    )
    openai_model: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-4.1-mini",
    )
    log_level: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )


settings = Settings()
