"""
3D Reconstruction router
Handles MapAnything integration for 3D scene generation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid
import asyncio
from datetime import datetime

router = APIRouter()

class ReconstructionRequest(BaseModel):
    job_id: str
    scene_id: str
    images: List[str]
    options: Optional[dict] = {}

class ReconstructionResponse(BaseModel):
    job_id: str
    status: str
    message: str

# In-memory job store (use Redis in production)
jobs = {}

@router.post("/3d-reconstruction", response_model=ReconstructionResponse)
async def reconstruct_3d(
    request: ReconstructionRequest,
    background_tasks: BackgroundTasks
):
    """
    Process 3D reconstruction using MapAnything
    Runs asynchronously in background
    """
    try:
        # Store job
        jobs[request.job_id] = {
            "status": "processing",
            "progress": 0,
            "started_at": datetime.utcnow(),
            "scene_id": request.scene_id
        }
        
        # Start background processing
        background_tasks.add_task(
            process_reconstruction,
            request.job_id,
            request.scene_id,
            request.images,
            request.options
        )
        
        return ReconstructionResponse(
            job_id=request.job_id,
            status="processing",
            message="3D reconstruction started"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_reconstruction(
    job_id: str,
    scene_id: str,
    images: List[str],
    options: dict
):
    """
    Background task for 3D reconstruction
    """
    try:
        # Import here to avoid loading during startup
        from app.services.reconstruction import MapAnythingReconstructor
        
        reconstructor = MapAnythingReconstructor()
        
        # Update progress
        jobs[job_id]["progress"] = 10
        
        # Process images
        result = await reconstructor.process(images, options)
        
        # Update job
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["result"] = result
        jobs[job_id]["completed_at"] = datetime.utcnow()
        
        # Notify API service via webhook
        await notify_completion(job_id, scene_id, result)
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        
        # Notify failure
        await notify_completion(job_id, scene_id, None, error=str(e))

async def notify_completion(job_id: str, scene_id: str, result: dict, error: str = None):
    """Notify API service of job completion"""
    import httpx
    from app.config import settings
    
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "job_id": job_id,
                "scene_id": scene_id,
                "status": "failed" if error else "completed",
                "result": result,
                "error_message": error
            }
            
            await client.post(
                f"{settings.API_SERVICE_URL}/api/v1/ai/internal/job-complete",
                json=payload,
                timeout=30.0
            )
    except Exception as e:
        print(f"Failed to notify API service: {e}")

@router.get("/3d-reconstruction/jobs/{job_id}/status")
def get_job_status(job_id: str):
    """Get reconstruction job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", 0),
        "result": job.get("result"),
        "error": job.get("error")
    }
