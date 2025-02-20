from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import json


class Settings(BaseSettings):
    API_V1_PREFIX: str
    PROJECT_NAME: str
    DEBUG: bool = False

    # Security
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str):
            return json.loads(v)
        return v

    # AI Model Settings
    OPENAI_API_KEY: str
    DEFAULT_MODEL: str
    VERIFICATION_MODEL: str

    # Database Settings
    CHROMA_PERSIST_DIRECTORY: str

    # Redis Settings
    REDIS_HOST: str
    REDIS_PORT: int

    # Cost Management
    COST_LIMIT: float

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
