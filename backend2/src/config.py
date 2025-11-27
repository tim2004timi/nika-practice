import os
from pydantic_settings import BaseSettings
from typing import Optional, Union
from functools import lru_cache

class Settings(BaseSettings): 
    # Database URL
    DATABASE_URL: str
    
    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10000
    
    # CORS settings (может быть строкой или списком)
    CORS_ORIGINS: Union[str, list] = "*"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'allow'
    


# Создаем экземпляр настроек
settings = Settings()

# Функция для dependency injection
@lru_cache()
def get_settings() -> Settings:
    return Settings()
