# API Service - REST API (FastAPI)

## Setup

```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run development
uvicorn app.main:app --reload --port 8001
```

## Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/aitwin
INFLUXDB_URL=http://localhost:8086
REDIS_URL=redis://localhost:6379
AI_SERVICE_URL=http://localhost:8000
SECRET_KEY=your-secret-key
```
