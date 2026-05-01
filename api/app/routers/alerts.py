"""
Alerts router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Alert, Equipment

router = APIRouter()

class AlertResponse(BaseModel):
    alert_id: str
    equipment_id: str
    severity: str
    status: str
    title: str
    description: Optional[str]
    triggered_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    equipment_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List alerts with filters"""
    query = db.query(Alert)
    
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    if equipment_id:
        equip = db.query(Equipment).filter(
            Equipment.equipment_id == equipment_id
        ).first()
        if equip:
            query = query.filter(Alert.equipment_id == equip.id)
    
    return query.order_by(Alert.triggered_at.desc()).all()

@router.get("/{alert_id}")
def get_alert(alert_id: str, db: Session = Depends(get_db)):
    """Get alert details"""
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "alert_id": alert.alert_id,
        "equipment": {
            "id": alert.equipment.equipment_id if alert.equipment else None,
            "name": alert.equipment.name if alert.equipment else None,
            "zone": alert.equipment.zone if alert.equipment else None
        },
        "severity": alert.severity,
        "status": alert.status,
        "title": alert.title,
        "description": alert.description,
        "root_cause": alert.root_cause,
        "recommended_actions": alert.recommended_actions,
        "confidence": alert.confidence,
        "anomaly_score": alert.anomaly_score,
        "sensor_values": alert.sensor_values,
        "triggered_at": alert.triggered_at
    }

@router.put("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str, db: Session = Depends(get_db)):
    """Acknowledge alert"""
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = "acknowledged"
    alert.acknowledged_at = datetime.utcnow()
    db.commit()
    
    return {"status": "success", "message": "Alert acknowledged"}

@router.put("/{alert_id}/resolve")
def resolve_alert(alert_id: str, db: Session = Depends(get_db)):
    """Resolve alert"""
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = "resolved"
    alert.resolved_at = datetime.utcnow()
    db.commit()
    
    return {"status": "success", "message": "Alert resolved"}
