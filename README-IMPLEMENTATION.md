# 🏭 AI Twin Factory - Complete Implementation

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Three.js](https://img.shields.io/badge/Three.js-black?style=flat&logo=three.js&logoColor=white)](https://threejs.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com/)

> Digital Twin Platform untuk Hilirisasi Industri Indonesia - **Proyek Pabrik Baja Nirkarat IMIP**

## 🎯 Overview

Platform **AI-powered Digital Twin** untuk monitoring dan maintenance prediktif fasilitas manufaktur. Implementasi lengkap dengan arsitektur **microservices** yang terpisah antara REST API, AI Backend, dan WebSocket service.

### Key Features
- 🤖 **AI-Driven 3D Reconstruction** - Generate digital twin dari foto menggunakan MapAnything
- 🔍 **Smart Anomaly Detection** - Hybrid ML (Statistical + Isolation Forest + LSTM)
- 🧠 **LLM Decision Agent** - AI assistant untuk maintenance recommendations
- 📡 **Real-time Monitoring** - WebSocket untuk live sensor streaming
- 🎨 **3D Visualization** - React Three Fiber untuk interactive digital twin

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Frontend   │  │   Web App    │  │   Mobile     │      │
│  │   (React)    │  │   (Operator) │  │   (Manager)  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    API GATEWAY (Nginx)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐  ┌─────────▼────────┐  ┌──────▼──────┐
│   REST API   │  │   AI Backend     │  │  WebSocket  │
│   Service    │  │   Service        │  │   Service   │
│  (FastAPI)   │  │   (FastAPI)      │  │  (Node.js)  │
│  Port: 8001  │  │   Port: 8000     │  │  Port: 3000 │
│  CPU-only    │  │   GPU-required   │  │  CPU-only   │
└───────┬──────┘  └─────────┬────────┘  └──────┬──────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼────────┐  ┌──────────▼─────────┐  ┌──▼──────────┐
│  PostgreSQL    │  │   InfluxDB         │  │    Redis    │
│  (Metadata)    │  │   (Time-series)    │  │   (Cache)   │
└────────────────┘  └────────────────────┘  └─────────────┘
```

## 📁 Project Structure

```
ai-twin-factory/
├── 📦 api/                     # REST API Service (FastAPI)
│   ├── app/
│   │   ├── main.py            # FastAPI app entry
│   │   ├── models.py          # Database models
│   │   ├── routers/           # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── equipment.py
│   │   │   ├── sensors.py
│   │   │   ├── alerts.py
│   │   │   ├── maintenance.py
│   │   │   ├── reconstruction.py
│   │   │   └── ai_proxy.py
│   │   └── dependencies.py    # Auth dependencies
│   ├── Dockerfile
│   └── requirements.txt
│
├── 🤖 ai/                      # AI Backend Service (FastAPI + GPU)
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── reconstruction.py     # MapAnything 3D
│   │   │   ├── anomaly_detection.py  # Isolation Forest
│   │   │   ├── llm_agent.py          # Qwen2.5 / Groq
│   │   │   └── health.py
│   │   └── services/
│   │       └── reconstruction.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── 🌐 websocket/               # WebSocket Service (Node.js)
│   ├── src/
│   │   └── server.js          # Socket.io server
│   ├── Dockerfile
│   └── package.json
│
├── 🎨 frontend/                # React + Vite Frontend
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   └── Layout.tsx
│   │   └── pages/
│   │       ├── Dashboard.tsx
│   │       ├── EquipmentList.tsx
│   │       ├── EquipmentDetail.tsx
│   │       ├── Alerts.tsx
│   │       ├── Reconstruction.tsx
│   │       └── Login.tsx
│   ├── index.html             # Contains dicoding meta tag ✅
│   ├── Dockerfile
│   └── package.json
│
├── 🐳 docker-compose.yml       # Full stack orchestration
└── 📖 docs/                    # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- NVIDIA Docker Runtime (for GPU support)
- Git

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd ai-twin-factory
```

### 2. Start All Services

```bash
# Start all services
docker-compose up -d

# Or start specific services
docker-compose up -d api ai frontend

# View logs
docker-compose logs -f api
```

### 3. Access Services

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React web app |
| API Docs | http://localhost:8001/docs | FastAPI Swagger UI |
| AI Docs | http://localhost:8000/docs | AI Service API docs |
| WebSocket | ws://localhost:3000 | Socket.io endpoint |
| Nginx | http://localhost | Reverse proxy (all services) |

### 4. Initialize Database

```bash
# Run database migrations
docker-compose exec api alembic upgrade head

# Create demo data
docker-compose exec api python -c "from app.database import init_db; init_db()"
```

## 🔧 Development

### Running Services Individually

#### API Service
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### AI Service
```bash
cd ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### WebSocket Service
```bash
cd websocket
npm install
npm run dev
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Authentication
```http
POST /api/v1/auth/login
POST /api/v1/auth/register
```

### Equipment
```http
GET    /api/v1/equipment           # List equipment
GET    /api/v1/equipment/{id}      # Get equipment detail
POST   /api/v1/equipment           # Create equipment
```

### Sensors
```http
GET    /api/v1/sensors/equipment/{id}/data      # Get sensor data
GET    /api/v1/sensors/equipment/{id}/latest   # Get latest readings
POST   /api/v1/sensors/ingest                   # Ingest sensor data (IoT)
```

### 3D Reconstruction
```http
POST   /api/v1/reconstruction/upload           # Upload photos
GET    /api/v1/reconstruction/jobs/{id}/status # Check job status
GET    /api/v1/reconstruction/scenes/{id}      # Get 3D scene
```

### Alerts
```http
GET    /api/v1/alerts              # List alerts
GET    /api/v1/alerts/{id}         # Get alert detail
PUT    /api/v1/alerts/{id}/acknowledge
PUT    /api/v1/alerts/{id}/resolve
```

### AI (Internal Proxy)
```http
POST   /api/v1/ai/detect-anomaly   # Anomaly detection
POST   /api/v1/ai/query            # Query LLM agent
```

## 🔌 WebSocket Events

### Client → Server
```javascript
socket.emit('subscribe-equipment', 'CONV-C03')
socket.emit('subscribe-zone', 'Zone 1')
socket.emit('unsubscribe', 'equipment:CONV-C03')
```

### Server → Client
```javascript
socket.on('sensor-data', (data) => {
  // Real-time sensor updates
})

socket.on('alert', (alert) => {
  // Alert notifications
})

socket.on('critical-alert', (alert) => {
  // Critical alerts (global broadcast)
})
```

## 🗄️ Database Schema

### PostgreSQL (Metadata)
- `users` - User accounts & authentication
- `equipment` - Equipment registry & 3D positions
- `scenes` - 3D scene files
- `alerts` - Alert history
- `work_orders` - Maintenance work orders
- `reconstruction_jobs` - 3D reconstruction jobs

### InfluxDB (Time-series)
- `sensor_data` - Real-time sensor readings
- Measurements: temperature, vibration, pressure, current

### Redis
- Session storage
- Job queues (Celery)
- Pub/Sub for WebSocket

## 🎨 Frontend Features

- **Dashboard** - Overview stats & recent alerts
- **Equipment List** - Browse equipment by zone
- **Equipment Detail** - Sensor data & maintenance info
- **3D Reconstruction** - Upload photos & generate digital twin
- **Alerts** - Manage & respond to alerts
- **Login** - Authentication

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Internal network isolation for AI service
- Rate limiting (via Nginx)

## 📊 Monitoring

Each service exposes health endpoints:
- API: `GET /health`
- AI: `GET /health` (includes GPU status)
- WebSocket: `GET /health` (includes connection count)

## 🚀 Deployment

### Production Checklist
- [ ] Change default passwords
- [ ] Configure SSL/TLS
- [ ] Set up proper secrets management
- [ ] Configure monitoring (Prometheus + Grafana)
- [ ] Set up log aggregation
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

### Environment Variables

Create `.env` files for each service:

**API Service (.env)**
```env
DATABASE_URL=postgresql://user:pass@postgres:5432/aitwin
SECRET_KEY=your-secret-key
AI_SERVICE_URL=http://ai:8000
```

**AI Service (.env)**
```env
API_SERVICE_URL=http://api:8001
OLLAMA_URL=http://ollama:11434
GROQ_API_KEY=your-groq-key
```

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- **MapAnything** (facebookresearch) - 3D reconstruction
- **Qwen2.5** (Alibaba) - Local LLM
- **FastAPI** - Web framework
- **Three.js** - 3D visualization

---

**Dikembangkan untuk mendukung Hilirisasi Industri Indonesia 🇮🇩**
