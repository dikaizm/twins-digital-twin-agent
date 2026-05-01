"""
Sensors router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from app.database import get_db
from app.models import Sensor, Equipment
from app.config import settings

router = APIRouter()

# InfluxDB client
influx_client = InfluxDBClient(
    url=settings.INFLUXDB_URL,
    token=settings.INFLUXDB_TOKEN,
    org=settings.INFLUXDB_ORG
)

class SensorDataPoint(BaseModel):
    timestamp: datetime
    value: float

class SensorIngestRequest(BaseModel):
    sensor_id: str
    equipment_id: str
    timestamp: datetime
    values: Dict[str, float]  # {temperature: 68.5, vibration: 4.2}

@router.get("/equipment/{equipment_id}/data")
def get_sensor_data(
    equipment_id: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get sensor data for equipment"""
    # Default to last 24 hours
    if not start:
        start = datetime.utcnow() - timedelta(hours=24)
    if not end:
        end = datetime.utcnow()
    
    # Get sensors for equipment
    equipment = db.query(Equipment).filter(
        Equipment.equipment_id == equipment_id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Query InfluxDB
    query_api = influx_client.query_api()
    
    data = {}
    for sensor in equipment.sensors:
        query = f'''
        from(bucket: "{settings.INFLUXDB_BUCKET}")
            |> range(start: {start.isoformat()}, stop: {end.isoformat()})
            |> filter(fn: (r) => r._measurement == "sensor_data")
            |> filter(fn: (r) => r.sensor_id == "{sensor.sensor_id}")
        '''
        
        tables = query_api.query(query)
        
        sensor_data = []
        for table in tables:
            for record in table.records:
                sensor_data.append({
                    "timestamp": record.get_time(),
                    "value": record.get_value()
                })
        
        data[sensor.type] = {
            "unit": sensor.unit,
            "data": sensor_data
        }
    
    return {
        "equipment_id": equipment_id,
        "time_range": {"start": start, "end": end},
        "sensors": data
    }

@router.post("/ingest")
def ingest_sensor_data(data: SensorIngestRequest):
    """
    Ingest sensor data from IoT gateway
    Called by MQTT subscriber or IoT gateway
    """
    try:
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)
        
        points = []
        for sensor_type, value in data.values.items():
            point = {
                "measurement": "sensor_data",
                "tags": {
                    "sensor_id": data.sensor_id,
                    "equipment_id": data.equipment_id,
                    "type": sensor_type
                },
                "fields": {
                    "value": value
                },
                "time": data.timestamp
            }
            points.append(point)
        
        write_api.write(bucket=settings.INFLUXDB_BUCKET, record=points)
        
        return {"status": "success", "points_written": len(points)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/equipment/{equipment_id}/latest")
def get_latest_sensor_data(equipment_id: str, db: Session = Depends(get_db)):
    """Get latest sensor readings for equipment"""
    query_api = influx_client.query_api()
    
    query = f'''
    from(bucket: "{settings.INFLUXDB_BUCKET}")
        |> range(start: -1m)
        |> filter(fn: (r) => r._measurement == "sensor_data")
        |> filter(fn: (r) => r.equipment_id == "{equipment_id}")
        |> last()
    '''
    
    tables = query_api.query(query)
    
    latest_data = {}
    for table in tables:
        for record in table.records:
            sensor_type = record.values.get("type")
            latest_data[sensor_type] = {
                "value": record.get_value(),
                "timestamp": record.get_time()
            }
    
    return {
        "equipment_id": equipment_id,
        "latest_readings": latest_data
    }
