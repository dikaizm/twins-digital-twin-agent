"""
Anomaly Detection router
Hybrid approach: Statistical + Isolation Forest + LSTM
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

router = APIRouter()

class AnomalyRequest(BaseModel):
    equipment_id: str
    sensor_data: Dict[str, float]  # {vibration: 12.5, temperature: 85.0}
    historical_context: bool = True

class AnomalyResponse(BaseModel):
    anomaly_detected: bool
    score: float
    severity: str
    contributing_factors: List[str]
    recommended_action: str

# Stage 1: Statistical threshold check
def check_statistical_thresholds(sensor_data: Dict[str, float]) -> tuple:
    """
    Check critical thresholds (instant response)
    Returns: (is_critical, factors)
    """
    critical_factors = []
    
    # Temperature thresholds
    if sensor_data.get("temperature", 0) > 100:
        critical_factors.append("temperature_critical")
    
    # Vibration thresholds
    if sensor_data.get("vibration", 0) > 10:
        critical_factors.append("vibration_critical")
    
    # Pressure thresholds
    if sensor_data.get("pressure", 0) < 2.0:  # Low pressure
        critical_factors.append("pressure_critical")
    
    return len(critical_factors) > 0, critical_factors

# Stage 2: Isolation Forest
def isolation_forest_detect(sensor_data: Dict[str, float]) -> tuple:
    """
    Isolation Forest for multi-variate anomalies
    """
    # In production, load pre-trained model
    # For demo, use simple heuristic
    
    # Normalize values (simplified)
    normalized = {
        "vibration": sensor_data.get("vibration", 0) / 10,  # 0-1
        "temperature": sensor_data.get("temperature", 0) / 100,  # 0-1
        "pressure": sensor_data.get("pressure", 5) / 5,  # 0-1
        "current": sensor_data.get("current", 50) / 50  # 0-1
    }
    
    # Calculate anomaly score (simplified)
    # In production, use actual Isolation Forest model
    score = sum([
        abs(normalized["vibration"] - 0.5) * 0.35,
        abs(normalized["temperature"] - 0.5) * 0.25,
        abs(normalized["pressure"] - 0.5) * 0.20,
        abs(normalized["current"] - 0.5) * 0.20
    ])
    
    # Contributing factors
    factors = []
    if normalized["vibration"] > 0.7:
        factors.append("vibration")
    if normalized["temperature"] > 0.7:
        factors.append("temperature")
    if normalized["pressure"] < 0.3:
        factors.append("pressure")
    if normalized["current"] > 0.8:
        factors.append("current")
    
    return score, factors

@router.post("/anomaly-detection", response_model=AnomalyResponse)
async def detect_anomaly(request: AnomalyRequest):
    """
    Detect anomalies using hybrid approach
    """
    try:
        # Stage 1: Statistical check (fast, critical)
        is_critical, critical_factors = check_statistical_thresholds(
            request.sensor_data
        )
        
        if is_critical:
            return AnomalyResponse(
                anomaly_detected=True,
                score=0.95,
                severity="CRITICAL",
                contributing_factors=critical_factors,
                recommended_action="immediate_inspection"
            )
        
        # Stage 2: Isolation Forest
        score, factors = isolation_forest_detect(request.sensor_data)
        
        # Determine severity
        if score > 0.9:
            severity = "CRITICAL"
        elif score > 0.7:
            severity = "HIGH"
        elif score > 0.5:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        # Recommended action based on severity
        actions = {
            "CRITICAL": "immediate_inspection",
            "HIGH": "schedule_maintenance_24h",
            "MEDIUM": "increase_monitoring",
            "LOW": "log_only"
        }
        
        return AnomalyResponse(
            anomaly_detected=score > 0.5,
            score=round(score, 2),
            severity=severity,
            contributing_factors=factors if factors else ["none"],
            recommended_action=actions[severity]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
