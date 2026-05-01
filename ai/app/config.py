"""
AI Service configuration
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """AI Service settings"""
    
    # App
    APP_NAME: str = "AI Twin Factory AI Service"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Model paths
    MODEL_PATH: str = "./models"
    MAPANYTHING_MODEL: str = "facebook/map-anything-apache"
    
    # LLM
    OLLAMA_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "qwen2.5:14b"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192"
    
    # Services
    API_SERVICE_URL: str = "http://localhost:8001"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Processing
    MAX_CONCURRENT_JOBS: int = 2
    GPU_MEMORY_FRACTION: float = 0.8
    
    # Anomaly Detection
    ANOMALY_THRESHOLD_LOW: float = 0.5
    ANOMALY_THRESHOLD_MEDIUM: float = 0.7
    ANOMALY_THRESHOLD_HIGH: float = 0.9
    
    class Config:
        env_file = ".env"

settings = Settings()
