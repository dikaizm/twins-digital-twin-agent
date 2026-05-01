"""
Health check router
"""

from fastapi import APIRouter
import torch

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-backend",
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_memory": get_gpu_memory()
    }

def get_gpu_memory():
    """Get GPU memory info"""
    if not torch.cuda.is_available():
        return None
    
    return {
        "allocated": torch.cuda.memory_allocated(0) / 1024**3,  # GB
        "cached": torch.cuda.memory_reserved(0) / 1024**3,  # GB
        "total": torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB
    }
