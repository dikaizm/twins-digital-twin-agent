"""
AI Proxy Router
Proxies requests to AI Backend Service
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import aiohttp

from app.config import settings

router = APIRouter()

class AnomalyDetectionRequest(BaseModel):
    equipment_id: str
    sensor_data: Dict[str, float]
    historical_context: bool = True

class AnomalyDetectionResponse(BaseModel):
    anomaly_detected: bool
    score: float
    severity: str
    contributing_factors: List[str]
    recommended_action: str

class LLMQueryRequest(BaseModel):
    query: str
    context: Optional[Dict] = None
    equipment_id: Optional[str] = None

class LLMQueryResponse(BaseModel):
    response: str
    actions: List[Dict]
    confidence: float

@router.post("/detect-anomaly", response_model=AnomalyDetectionResponse)
async def detect_anomaly(request: AnomalyDetectionRequest):
    """
    Proxy anomaly detection request to AI service
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.AI_SERVICE_URL}/internal/anomaly-detection",
                json=request.dict(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return AnomalyDetectionResponse(**result)
                else:
                    raise HTTPException(
                        status_code=500, 
                        detail="AI service error"
                    )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")

@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest):
    """
    Proxy LLM query to AI service
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.AI_SERVICE_URL}/internal/llm-agent",
                json=request.dict(),
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return LLMQueryResponse(**result)
                else:
                    raise HTTPException(
                        status_code=500,
                        detail="AI service error"
                    )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")

@router.post("/internal/job-complete")
async def job_complete_webhook(data: dict):
    """
    Webhook called by AI service when job is complete
    """
    # Update database with results
    # This would typically update the ReconstructionJob and Scene records
    from app.database import SessionLocal
    from app.models import ReconstructionJob, Scene
    
    db = SessionLocal()
    try:
        job = db.query(ReconstructionJob).filter(
            ReconstructionJob.job_id == data.get("job_id")
        ).first()
        
        if job:
            job.status = data.get("status", "completed")
            job.result_data = data.get("result", {})
            job.progress_percent = 100
            job.completed_at = datetime.utcnow()
            
            # Update scene if available
            if job.scene and data.get("result"):
                result = data["result"]
                job.scene.glb_url = result.get("scene_url")
                job.scene.metadata_url = result.get("metadata_url")
                job.scene.status = "completed"
            
            db.commit()
        
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

from datetime import datetime
