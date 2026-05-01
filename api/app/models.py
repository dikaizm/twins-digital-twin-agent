"""
Database models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    role = Column(String(50), default="operator")  # admin, operator, manager
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(String(100), unique=True, index=True)  # e.g., CONV-C03
    name = Column(String(255))
    type = Column(String(100))  # conveyor, motor, pump, furnace
    zone = Column(String(100))  # Zone 1, Zone 2, etc.
    description = Column(Text)
    manufacturer = Column(String(255))
    model = Column(String(255))
    install_date = Column(DateTime)
    last_maintenance = Column(DateTime)
    next_scheduled_maintenance = Column(DateTime)
    status = Column(String(50), default="operational")  # operational, maintenance, offline
    
    # 3D Position
    position_x = Column(Float)
    position_y = Column(Float)
    position_z = Column(Float)
    rotation_x = Column(Float)
    rotation_y = Column(Float)
    rotation_z = Column(Float)
    scale = Column(Float, default=1.0)
    
    # Asset
    asset_path = Column(String(500))
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    
    # Thresholds
    threshold_config = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scene = relationship("Scene", back_populates="equipment")
    sensors = relationship("Sensor", back_populates="equipment")
    alerts = relationship("Alert", back_populates="equipment")

class Scene(Base):
    __tablename__ = "scenes"
    
    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    description = Column(Text)
    factory_id = Column(String(100))
    zone = Column(String(100))
    
    # 3D Assets
    glb_url = Column(String(500))
    metadata_url = Column(String(500))
    thumbnail_url = Column(String(500))
    
    # Status
    status = Column(String(50), default="processing")  # processing, completed, failed
    
    # Source
    source_images = Column(JSON, default=[])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="scene")
    reconstruction_jobs = relationship("ReconstructionJob", back_populates="scene")

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    type = Column(String(100))  # temperature, vibration, pressure, current
    unit = Column(String(50))  # celsius, mm/s, bar, ampere
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    
    # Configuration
    sampling_rate = Column(Integer)  # Hz
    location = Column(String(255))  # physical location on equipment
    
    # Thresholds
    warning_threshold = Column(Float)
    critical_threshold = Column(Float)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="sensors")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(100), unique=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    
    # Alert details
    severity = Column(String(50))  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), default="open")  # open, acknowledged, resolved
    title = Column(String(500))
    description = Column(Text)
    
    # AI Analysis
    root_cause = Column(Text)
    recommended_actions = Column(JSON, default=[])
    confidence = Column(Float)
    
    # Metrics
    anomaly_score = Column(Float)
    sensor_values = Column(JSON, default={})
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey("users.id"))
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    triggered_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="alerts")

class WorkOrder(Base):
    __tablename__ = "work_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    wo_number = Column(String(100), unique=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    
    # Work order details
    title = Column(String(500))
    description = Column(Text)
    priority = Column(String(50))  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), default="open")  # open, in_progress, completed, cancelled
    
    # Assignment
    requested_by = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))
    
    # Scheduling
    scheduled_date = Column(DateTime)
    estimated_duration = Column(Integer)  # minutes
    actual_duration = Column(Integer)
    
    # Materials
    required_parts = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

class ReconstructionJob(Base):
    __tablename__ = "reconstruction_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), unique=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    
    # Job details
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    job_type = Column(String(100), default="3d_reconstruction")
    
    # Source
    input_images = Column(JSON, default=[])
    
    # Results
    result_data = Column(JSON, default={})
    error_message = Column(Text)
    
    # Progress
    progress_percent = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relationships
    scene = relationship("Scene", back_populates="reconstruction_jobs")

class UserActivity(Base):
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))
    entity_type = Column(String(100))  # equipment, alert, work_order
    entity_id = Column(String(100))
    details = Column(JSON, default={})
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
