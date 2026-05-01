"""
Configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "AI Twin Factory API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/aitwin"
    
    # InfluxDB (Time-series)
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = "admin-token"
    INFLUXDB_ORG: str = "ai-twin"
    INFLUXDB_BUCKET: str = "sensor_data"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI Service
    AI_SERVICE_URL: str = "http://localhost:8000"
    AI_SERVICE_TIMEOUT: int = 300
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:4173"
    ]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # S3 (optional)
    S3_BUCKET: str = "ai-twin-assets"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
