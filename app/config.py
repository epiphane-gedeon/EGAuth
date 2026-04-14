from pydantic_settings import BaseSettings
from functools import lru_cache
 
class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://user:pass@localhost/egauth'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PRIVATE_KEY_PATH: str = 'keys/private.pem'
    PUBLIC_KEY_PATH: str  = 'keys/public.pem'
    class Config:
        env_file = '.env'
 
@lru_cache()
def get_settings(): return Settings()
