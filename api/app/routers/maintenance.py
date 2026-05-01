"""
Maintenance router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import WorkOrder, Equipment

router = APIRouter()

class WorkOrderCreate(BaseModel):
    equipment_id: str
    title: str
    description: str
    priority: str  # LOW, MEDIUM, HIGH, CRITICAL
    scheduled_date: Optional[datetime] = None
    estimated_duration: Optional[int] = None  # minutes

class WorkOrderResponse(WorkOrderCreate):
    id: int
    wo_number: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/work-orders", response_model=List[WorkOrderResponse])
def list_work_orders(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List work orders"""
    query = db.query(WorkOrder)
    
    if status:
        query = query.filter(WorkOrder.status == status)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    
    return query.order_by(WorkOrder.created_at.desc()).all()

@router.post("/work-orders", response_model=WorkOrderResponse)
def create_work_order(
    data: WorkOrderCreate,
    db: Session = Depends(get_db)
):
    """Create new work order"""
    # Get equipment
    equipment = db.query(Equipment).filter(
        Equipment.equipment_id == data.equipment_id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Generate WO number
    wo_count = db.query(WorkOrder).count()
    wo_number = f"WO-{datetime.utcnow().year}-{wo_count + 1:05d}"
    
    work_order = WorkOrder(
        wo_number=wo_number,
        equipment_id=equipment.id,
        title=data.title,
        description=data.description,
        priority=data.priority,
        scheduled_date=data.scheduled_date,
        estimated_duration=data.estimated_duration,
        status="open"
    )
    
    db.add(work_order)
    db.commit()
    db.refresh(work_order)
    
    return work_order

@router.get("/work-orders/{wo_number}")
def get_work_order(wo_number: str, db: Session = Depends(get_db)):
    """Get work order details"""
    wo = db.query(WorkOrder).filter(WorkOrder.wo_number == wo_number).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    return {
        "wo_number": wo.wo_number,
        "equipment": {
            "id": wo.equipment.equipment_id if wo.equipment else None,
            "name": wo.equipment.name if wo.equipment else None
        },
        "title": wo.title,
        "description": wo.description,
        "priority": wo.priority,
        "status": wo.status,
        "scheduled_date": wo.scheduled_date,
        "estimated_duration": wo.estimated_duration,
        "created_at": wo.created_at
    }

@router.put("/work-orders/{wo_number}/complete")
def complete_work_order(wo_number: str, db: Session = Depends(get_db)):
    """Mark work order as completed"""
    wo = db.query(WorkOrder).filter(WorkOrder.wo_number == wo_number).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    wo.status = "completed"
    wo.completed_at = datetime.utcnow()
    db.commit()
    
    return {"status": "success", "message": "Work order completed"}
