from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/movie_warehouse"
    DATABASE_ECHO: bool = True  # Set to False in production
    
    # Connection Pool Settings
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 3600
    
    # TMDb API
    TMDB_API_KEY: str = ""
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    
    # Google Gemini API (optional)
    GEMINI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()