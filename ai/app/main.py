"""
AI Twin Factory - AI Backend Service
Handles ML/AI computations: 3D reconstruction, anomaly detection, LLM agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
import torch

from app.config import settings
from app.routers import reconstruction, anomaly_detection, llm_agent, health

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting AI Backend Service",
                version="1.0.0",
                cuda_available=torch.cuda.is_available(),
                cuda_devices=torch.cuda.device_count() if torch.cuda.is_available() else 0)
    
    # Preload models (optional, can also lazy load)
    # This ensures first request isn't slow
    logger.info("Preloading models...")
    # await preload_models()
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Backend Service")

app = FastAPI(
    title="AI Twin Factory - AI Backend Service",
    description="ML/AI processing service for Digital Twin Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware (internal only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Only API service
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reconstruction.router, prefix="/internal", tags=["3D Reconstruction"])
app.include_router(anomaly_detection.router, prefix="/internal", tags=["Anomaly Detection"])
app.include_router(llm_agent.router, prefix="/internal", tags=["LLM Agent"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Twin Factory - AI Backend Service",
        "version": "1.0.0",
        "gpu_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "docs": "/docs"
    }
