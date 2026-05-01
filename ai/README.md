# AI Backend Service - FastAPI

## Setup

```bash
cd ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download models
python scripts/download_models.py

# Run development
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

```bash
MODEL_PATH=./models
REDIS_URL=redis://localhost:6379
API_SERVICE_URL=http://localhost:8001
OLLAMA_URL=http://localhost:11434
GROQ_API_KEY=your-groq-key
```

## GPU Requirements

- Minimum: NVIDIA GPU with 8GB VRAM
- Recommended: RTX 4090 (24GB VRAM)
- CUDA: 11.8+
