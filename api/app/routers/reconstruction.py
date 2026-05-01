"""
3D Reconstruction router
Handles photo uploads and 3D scene generation jobs
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import uuid
import os
import aiohttp
import asyncio

from app.database import get_db
from app.models import ReconstructionJob, Scene
from app.config import settings
from app.dependencies import get_current_user

router = APIRouter()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

class ReconstructionRequest(BaseModel):
    name: str
    description: Optional[str] = None
    zone: str
    factory_id: str = "IMIP-01"

class ReconstructionResponse(BaseModel):
    job_id: str
    status: str
    message: str
    estimated_time: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress_percent: int
    result: Optional[dict] = None
    error_message: Optional[str] = None

@router.post("/upload", response_model=ReconstructionResponse)
async def upload_photos(
    files: List[UploadFile] = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    zone: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload photos for 3D reconstruction
    Creates a job and submits to AI service for processing
    """
    # Generate unique IDs
    job_id = str(uuid.uuid4())
    scene_id = f"SCENE-{uuid.uuid4().hex[:8].upper()}"
    
    # Save uploaded files
    saved_files = []
    for file in files:
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.content_type}")
        
        file_path = f"{settings.UPLOAD_DIR}/{job_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        saved_files.append(file_path)
    
    # Create scene record
    scene = Scene(
        scene_id=scene_id,
        name=name,
        description=description,
        zone=zone,
        factory_id="IMIP-01",
        status="processing",
        source_images=saved_files
    )
    db.add(scene)
    
    # Create job record
    job = ReconstructionJob(
        job_id=job_id,
        scene_id=scene.id,
        status="pending",
        job_type="3d_reconstruction",
        input_images=saved_files,
        progress_percent=0
    )
    db.add(job)
    db.commit()
    
    # Submit to AI service asynchronously (don't wait)
    asyncio.create_task(submit_to_ai_service(job_id, saved_files, scene_id))
    
    return ReconstructionResponse(
        job_id=job_id,
        status="pending",
        message="Photos uploaded successfully. 3D reconstruction started.",
        estimated_time="2-5 minutes"
    )

async def submit_to_ai_service(job_id: str, image_paths: List[str], scene_id: str):
    """Submit job to AI backend service"""
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "job_id": job_id,
                "scene_id": scene_id,
                "images": image_paths,
                "options": {
                    "quality": "high",
                    "export_format": "glb"
                }
            }
            
            async with session.post(
                f"{settings.AI_SERVICE_URL}/internal/3d-reconstruction",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=300)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # Update job status via webhook or polling
                else:
                    # Handle error
                    pass
    except Exception as e:
        # Log error and update job status
        print(f"Error submitting to AI service: {e}")

@router.get("/jobs/{job_id}/status", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """Get reconstruction job status"""
    job = db.query(ReconstructionJob).filter(ReconstructionJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        progress_percent=job.progress_percent,
        result=job.result_data,
        error_message=job.error_message
    )

@router.get("/scenes/{scene_id}")
def get_scene(scene_id: str, db: Session = Depends(get_db)):
    """Get 3D scene by ID"""
    scene = db.query(Scene).filter(Scene.scene_id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    return {
        "scene_id": scene.scene_id,
        "name": scene.name,
        "description": scene.description,
        "zone": scene.zone,
        "status": scene.status,
        "glb_url": scene.glb_url,
        "metadata_url": scene.metadata_url,
        "thumbnail_url": scene.thumbnail_url,
        "created_at": scene.created_at
    }

@router.get("/scenes/{scene_id}/equipment")
def get_scene_equipment(scene_id: str, db: Session = Depends(get_db)):
    """Get all equipment in a scene"""
    scene = db.query(Scene).filter(Scene.scene_id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    
    equipment_list = []
    for eq in scene.equipment:
        equipment_list.append({
            "equipment_id": eq.equipment_id,
            "name": eq.name,
            "type": eq.type,
            "position": [eq.position_x, eq.position_y, eq.position_z],
            "rotation": [eq.rotation_x, eq.rotation_y, eq.rotation_z],
            "asset_path": eq.asset_path
        })
    
    return {"scene_id": scene_id, "equipment": equipment_list}
