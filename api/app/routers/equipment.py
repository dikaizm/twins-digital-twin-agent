"""
Equipment router
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models import Equipment, Scene
from app.dependencies import get_current_user

router = APIRouter()

# Pydantic models
class EquipmentCreate(BaseModel):
    equipment_id: str
    name: str
    type: str
    zone: str
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None

class EquipmentResponse(EquipmentCreate):
    id: int
    status: str
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    position_z: Optional[float] = None
    asset_path: Optional[str] = None
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[EquipmentResponse])
def list_equipment(
    zone: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all equipment with optional filters"""
    query = db.query(Equipment)
    
    if zone:
        query = query.filter(Equipment.zone == zone)
    if type:
        query = query.filter(Equipment.type == type)
    if status:
        query = query.filter(Equipment.status == status)
    
    return query.all()

@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: str, db: Session = Depends(get_db)):
    """Get equipment by ID"""
    equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.post("/", response_model=EquipmentResponse)
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db)
):
    """Create new equipment"""
    db_equipment = Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.get("/zones/list")
def list_zones(db: Session = Depends(get_db)):
    """List all unique zones"""
    zones = db.query(Equipment.zone).distinct().all()
    return [z[0] for z in zones if z[0]]
