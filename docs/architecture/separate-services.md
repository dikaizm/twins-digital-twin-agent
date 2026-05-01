# 🏗️ Backend Architecture: Separate Services (Option A)

## Overview

Arsitektur ini memisahkan **REST API Service** dan **AI Backend Service** sebagai independent services yang berkomunikasi via internal network.

**Keputusan:** Option A - Separate Services  
**Alasan:** Scalability, fault isolation, dan optimal resource utilization untuk production-grade deployment.

---

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Web App    │  │  Mobile App  │  │   Tablet     │              │
│  │  (Operator)  │  │  (Manager)   │  │  (Control)   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼─────────────────┼─────────────────┼──────────────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Nginx/Kong)                        │
│         • Rate limiting • Auth • Load balancing • SSL                │
└─────────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
┌───────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   REST API    │  │   AI Backend    │  │   WebSocket     │
│   SERVICE     │  │    SERVICE      │  │    SERVICE      │
│  (Node.js/    │  │   (Python/      │  │   (Node.js/     │
│   FastAPI)    │  │   FastAPI)      │  │   Socket.io)    │
├───────────────┤  ├─────────────────┤  ├─────────────────┤
│ Port: 3001    │  │ Port: 8000      │  │ Port: 3002      │
│ CPU: 2 cores  │  │ GPU: RTX 4090   │  │ CPU: 2 cores    │
│ RAM: 4 GB     │  │ RAM: 16 GB      │  │ RAM: 4 GB       │
└───────┬───────┘  └────────┬────────┘  └────────┬────────┘
        │                   │                    │
        │    ┌──────────────┴────────────────────┘
        │    │
        │    │  Internal Network (Docker Network / VPC)
        │    │
        ▼    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  PostgreSQL  │  │  InfluxDB    │  │     S3       │              │
│  │   (Metadata) │  │ (Time-series)│  │  (3D Assets) │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Service 1: REST API Service

### Responsibility
- Authentication & Authorization (JWT)
- User management & RBAC
- CRUD operations (equipment, alerts, maintenance logs)
- File upload handling
- API Gateway functions
- Business logic coordination
- Calling AI Service untuk heavy computation

### Tech Stack
```yaml
Language: Node.js (TypeScript) atau Python (FastAPI)
Framework: 
  - Option A: NestJS (Node.js) - Enterprise-grade
  - Option B: FastAPI (Python) - Simpler, async-native

Database Clients:
  - PostgreSQL: Prisma ORM / SQLAlchemy
  - InfluxDB: @influxdata/influxdb-client
  
Cache: Redis (for sessions, rate limiting)
Auth: Passport.js (Node) atau FastAPI JWT
Validation: Zod / class-validator / Pydantic
Documentation: Swagger/OpenAPI
```

### API Endpoints Structure
```
/api/v1/
├── auth/
│   ├── POST /login
│   ├── POST /register
│   ├── POST /refresh
│   └── POST /logout
├── users/
│   ├── GET /me
│   ├── PUT /me
│   └── GET /:id (admin only)
├── equipment/
│   ├── GET / (list)
│   ├── GET /:id
│   ├── POST / (create)
│   ├── PUT /:id
│   └── DELETE /:id
├── sensors/
│   ├── GET /:equipmentId/data (query time-range)
│   └── POST /ingest (from IoT gateway)
├── alerts/
│   ├── GET / (list with filters)
│   ├── GET /:id
│   ├── PUT /:id/acknowledge
│   └── POST / (create from AI service)
├── maintenance/
│   ├── GET /work-orders
│   ├── POST /work-orders
│   └── PUT /work-orders/:id/complete
├── reconstruction/
│   ├── POST /upload-photos
│   ├── GET /jobs/:id/status
│   └── GET /jobs/:id/result
└── ai/
    ├── POST /query (chat dengan AI agent)
    └── GET /recommendations/:equipmentId
```

### Key Implementation
```typescript
// Node.js/NestJS Example
@Controller('api/v1/reconstruction')
export class ReconstructionController {
  constructor(
    private readonly aiService: AIServiceClient,
    private readonly jobRepository: JobRepository,
  ) {}

  @Post('upload-photos')
  async uploadPhotos(
    @UploadedFiles() files: Express.Multer.File[],
    @Body() metadata: UploadMetadataDto,
  ) {
    // 1. Save upload ke DB
    const job = await this.jobRepository.create({
      type: '3D_RECONSTRUCTION',
      status: 'PENDING',
      files: files.map(f => f.path),
    });

    // 2. Call AI Service asynchronously
    this.aiService.submitReconstructionJob({
      jobId: job.id,
      files: files.map(f => f.path),
      metadata,
    });

    // 3. Return immediately dengan jobId
    return {
      jobId: job.id,
      status: 'PROCESSING',
      estimatedTime: '2-5 minutes',
    };
  }
}
```

---

## 🤖 Service 2: AI Backend Service

### Responsibility
- 3D Reconstruction (MapAnything)
- Anomaly Detection (Isolation Forest + LSTM)
- LLM Decision Agent (Qwen2.5 / Groq)
- Heavy ML computation
- GPU-intensive tasks

### Tech Stack
```yaml
Language: Python 3.11+
Framework: FastAPI

ML/DL:
  - PyTorch (2.0+)
  - Transformers (HuggingFace)
  - scikit-learn
  - LangGraph / LangChain

3D Processing:
  - MapAnything (facebookresearch)
  - Open3D
  - trimesh

LLM:
  - Ollama (local Qwen2.5)
  - Groq API (alternative)
  - ChromaDB (RAG)

Monitoring:
  - Prometheus (metrics)
  - Grafana (visualization)
```

### Internal API Structure
```python
# FastAI Service Endpoints (internal only)
@app.post("/internal/3d-reconstruction")
async def reconstruct_3d(request: ReconstructionRequest):
    """
    Process 3D reconstruction menggunakan MapAnything
    """
    # Heavy GPU computation here
    result = await mapanything_pipeline.process(request.images)
    return result

@app.post("/internal/anomaly-detection")
async def detect_anomaly(request: AnomalyRequest):
    """
    Run anomaly detection pada sensor data
    """
    result = await anomaly_pipeline.detect(request.sensor_data)
    return result

@app.post("/internal/llm-agent")
async def llm_agent(request: AgentRequest):
    """
    Query LLM decision agent
    """
    response = await agent_executor.invoke(request.context)
    return response

@app.get("/internal/health")
async def health_check():
    """
    Health check untuk monitoring
    """
    return {
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "gpu_memory": get_gpu_memory(),
    }
```

### Queue-Based Processing
```python
# Menggunakan Celery + Redis untuk async processing
from celery import Celery

app = Celery('ai_tasks', broker='redis://localhost:6379')

@app.task(bind=True, max_retries=3)
def process_3d_reconstruction(self, job_id: str, image_paths: List[str]):
    """
    Background task untuk 3D reconstruction
    """
    try:
        # Update status: PROCESSING
        update_job_status(job_id, "PROCESSING")
        
        # Heavy computation
        result = mapanything_pipeline.process(image_paths)
        
        # Save result ke S3
        s3_url = upload_to_s3(result.glb_file)
        
        # Update DB via API service
        notify_api_service(job_id, "COMPLETED", s3_url)
        
    except Exception as exc:
        # Retry dengan exponential backoff
        self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

---

## 🌐 Service 3: WebSocket Service (Optional Separate)

### Responsibility
- Real-time sensor data streaming
- Live dashboard updates
- Alert broadcasting
- Low-latency communication

### Tech Stack
```yaml
Language: Node.js (TypeScript)
Framework: Socket.io

Pub/Sub: Redis Adapter (untuk multi-instance scaling)
Authentication: JWT validation
```

### Events
```typescript
// Server → Client
io.emit('sensor-data', {
  equipmentId: 'CONV-C03',
  timestamp: '2026-04-30T12:00:00Z',
  sensors: {
    vibration: 4.2,
    temperature: 68,
    current: 32.5
  }
});

io.emit('alert', {
  id: 'alert-001',
  severity: 'CRITICAL',
  equipmentId: 'CONV-C03',
  message: 'Vibration exceeds threshold',
  timestamp: '2026-04-30T12:05:00Z'
});

// Client → Server
socket.on('subscribe-equipment', (equipmentId) => {
  socket.join(`equipment:${equipmentId}`);
});
```

---

## 🔌 Inter-Service Communication

### 1. Synchronous (REST API → AI Service)
```typescript
// REST API Service calling AI Service
class AIServiceClient {
  private baseURL = 'http://ai-service:8000/internal';
  
  async submitReconstructionJob(data: ReconstructionJob) {
    const response = await fetch(`${this.baseURL}/3d-reconstruction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  }
  
  async detectAnomaly(sensorData: SensorData) {
    const response = await fetch(`${this.baseURL}/anomaly-detection`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sensor_data: sensorData }),
    });
    return response.json();
  }
}
```

### 2. Asynchronous (Message Queue)
```yaml
# Redis / RabbitMQ untuk async processing

Flow:
  1. API Service publish job ke queue
  2. AI Service consume dari queue
  3. AI Service process (GPU intensive)
  4. AI Service publish result ke queue
  5. API Service consume result, update DB

Benefits:
  - Decoupling
  - Load balancing (multiple AI workers)
  - Retry mechanism
  - Durability
```

### 3. Webhook / Callback
```python
# AI Service notify API Service via webhook
async def notify_job_complete(job_id: str, result: dict):
    async with aiohttp.ClientSession() as session:
        await session.post(
            'http://api-service:3001/api/v1/internal/job-complete',
            json={
                'job_id': job_id,
                'status': 'COMPLETED',
                'result': result
            }
        )
```

---

## 🐳 Docker Compose Setup

```yaml
version: '3.8'

services:
  # Service 1: REST API
  api-service:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: ai-twin-api
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - PORT=3001
      - DATABASE_URL=postgresql://user:pass@postgres:5432/aitwin
      - INFLUXDB_URL=http://influxdb:8086
      - AI_SERVICE_URL=http://ai-service:8000
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
      - influxdb
    networks:
      - ai-twin-network
    restart: unless-stopped

  # Service 2: AI Backend
  ai-service:
    build:
      context: ./ai
      dockerfile: Dockerfile
    container_name: ai-twin-ai
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
      - MODEL_PATH=/models
      - REDIS_URL=redis://redis:6379
      - API_SERVICE_URL=http://api-service:3001
    volumes:
      - ./models:/models:ro
      - ai-cache:/app/cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      - redis
    networks:
      - ai-twin-network
    restart: unless-stopped

  # Service 3: WebSocket (optional, bisa juga di API service)
  websocket-service:
    build:
      context: ./websocket
      dockerfile: Dockerfile
    container_name: ai-twin-ws
    ports:
      - "3002:3002"
    environment:
      - PORT=3002
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    networks:
      - ai-twin-network
    restart: unless-stopped

  # Supporting Services
  postgres:
    image: postgres:15-alpine
    container_name: ai-twin-postgres
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=aitwin
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - ai-twin-network

  redis:
    image: redis:7-alpine
    container_name: ai-twin-redis
    volumes:
      - redis-data:/data
    networks:
      - ai-twin-network

  influxdb:
    image: influxdb:2.7
    container_name: ai-twin-influx
    environment:
      - INFLUXDB_DB=sensor_data
      - INFLUXDB_ADMIN_USER=admin
      - INFLUXDB_ADMIN_PASSWORD=adminpass
    volumes:
      - influxdb-data:/var/lib/influxdb2
    networks:
      - ai-twin-network

  nginx:
    image: nginx:alpine
    container_name: ai-twin-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api-service
      - ai-service
      - websocket-service
    networks:
      - ai-twin-network
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:
  influxdb-data:
  ai-cache:

networks:
  ai-twin-network:
    driver: bridge
```

---

## 📊 Resource Allocation

### Development Environment (Hackathon)
```
Machine: 1x High-end workstation / Cloud VM

Resources:
  API Service:    2 CPU, 4 GB RAM
  AI Service:     4 CPU, 16 GB RAM, 1x GPU (RTX 4090)
  WebSocket:      2 CPU, 4 GB RAM
  Databases:      2 CPU, 4 GB RAM
  -------------------------------------
  Total:          10 CPU, 28 GB RAM, 1x GPU
```

### Production Environment
```
API Service:      2-4 replicas, CPU-optimized instances
AI Service:       1-2 replicas, GPU instances (auto-scale)
WebSocket:        2-4 replicas, CPU-optimized instances
Databases:        Managed services (RDS, InfluxDB Cloud)
```

---

## 🚀 Deployment Checklist

### Local Development
- [ ] Docker & Docker Compose installed
- [ ] NVIDIA Docker runtime (for GPU)
- [ ] Clone all service repositories
- [ ] Setup environment variables
- [ ] Run `docker-compose up`
- [ ] Verify all services healthy
- [ ] Test inter-service communication

### Production
- [ ] Kubernetes cluster setup
- [ ] GPU node pool configured
- [ ] Secrets management (K8s secrets / Vault)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Logging (ELK stack / Loki)
- [ ] Backup strategy

---

## 📝 API Contract Between Services

### AI Service Input/Output

**POST /internal/3d-reconstruction**
```json
// Request
{
  "job_id": "uuid-v4",
  "images": [
    "/uploads/photo1.jpg",
    "/uploads/photo2.jpg"
  ],
  "options": {
    "quality": "high",
    "export_format": "glb"
  }
}

// Response (async)
{
  "job_id": "uuid-v4",
  "status": "PROCESSING",
  "estimated_time": "120s"
}

// Webhook callback
{
  "job_id": "uuid-v4",
  "status": "COMPLETED",
  "result": {
    "scene_url": "s3://bucket/scene.glb",
    "metadata": {
      "equipment_count": 12,
      "confidence": 0.89
    }
  }
}
```

**POST /internal/anomaly-detection**
```json
// Request
{
  "equipment_id": "CONV-C03",
  "sensor_data": {
    "timestamp": "2026-04-30T12:00:00Z",
    "vibration": 12.5,
    "temperature": 85,
    "current": 45.2
  },
  "historical_context": true
}

// Response (sync)
{
  "anomaly_detected": true,
  "score": 0.94,
  "severity": "CRITICAL",
  "contributing_factors": ["vibration", "temperature"],
  "recommended_action": "immediate_inspection"
}
```

---

## 🔒 Security Considerations

1. **Internal Network Isolation**
   - AI Service tidak expose ke public
   - Hanya bisa diakses dari API Service (internal network)

2. **Authentication**
   - Service-to-service: API keys atau mTLS
   - Client: JWT tokens

3. **Rate Limiting**
   - AI Service: Limit berdasarkan GPU capacity
   - API Service: Standard rate limiting per user

4. **Data Privacy**
   - Factory data tidak keluar dari VPC
   - LLM bisa on-premise (Ollama) atau API dengan data protection

---

## 📈 Monitoring & Observability

### Metrics to Track
- API Service: Request latency, error rate, throughput
- AI Service: GPU utilization, queue length, processing time
- WebSocket: Connected clients, message throughput
- Database: Query latency, connection pool

### Logging Strategy
- Structured logging (JSON)
- Correlation IDs untuk tracing request across services
- Centralized log aggregation

---

**Status:** ✅ Architecture defined  
**Next:** Implementasi service per service (start dengan API, kemudian AI)
