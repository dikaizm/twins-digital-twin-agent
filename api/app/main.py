"""
AI Twin Factory - REST API Service
Main FastAPI application
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import structlog

from app.config import settings
from app.database import engine, Base
from app.routers import auth, equipment, sensors, alerts, maintenance, reconstruction, ai_proxy
from app.dependencies import get_current_user

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting API Service", 
                version="1.0.0", 
                environment=settings.ENVIRONMENT)
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    logger.info("Shutting down API Service")

app = FastAPI(
    title="AI Twin Factory - API Service",
    description="REST API for Digital Twin Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    equipment.router, 
    prefix="/api/v1/equipment", 
    tags=["Equipment"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    sensors.router, 
    prefix="/api/v1/sensors", 
    tags=["Sensors"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    alerts.router, 
    prefix="/api/v1/alerts", 
    tags=["Alerts"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    maintenance.router, 
    prefix="/api/v1/maintenance", 
    tags=["Maintenance"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    reconstruction.router, 
    prefix="/api/v1/reconstruction", 
    tags=["3D Reconstruction"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    ai_proxy.router, 
    prefix="/api/v1/ai", 
    tags=["AI Proxy"],
    dependencies=[Depends(get_current_user)]
)

# Static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "api",
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "AI Twin Factory - API Service",
        "version": "1.0.0",
        "docs": "/docs"
    }
