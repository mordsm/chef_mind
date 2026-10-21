from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Principal(BaseModel):
    user_id: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9_-]+$")
    role: Literal["reviewer", "cook"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHEF_", env_file=".env", extra="ignore")
    database_url: str = "postgresql+psycopg://chef:local-development-only@127.0.0.1:56432/chef"
    vault_root: Path = Path("vault")
    api_keys: dict[str, Principal] = Field(default_factory=dict)
    poll_seconds: int = Field(default=10, ge=1, le=3600)
    sync_enabled: bool = False
    model_enabled: bool = False
    model_name: str = "gpt-6-luna"
    openai_api_key: SecretStr | None = None
    model_timeout_seconds: float = Field(default=20, ge=1, le=60)
    model_max_output_tokens: int = Field(default=400, ge=100, le=2000)
    model_calls_per_minute: int = Field(default=30, ge=1, le=1200)
    model_user_calls_per_minute: int = Field(default=10, ge=1, le=1200)

    @model_validator(mode="after")
    def check_tokens(self):
        if any(len(key) < 24 or not key.isascii() or any(c.isspace() for c in key) for key in self.api_keys):
            raise ValueError("API tokens must contain at least 24 ASCII characters without whitespace")
        return self


@lru_cache
def get_settings():
    return Settings()
