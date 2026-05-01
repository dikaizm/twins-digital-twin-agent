# AI Twin Factory - Complete Implementation

## 🏗️ Project Structure

```
ai-twin-factory/
├── api/                    # REST API Service (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── dependencies.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic/
│
├── ai/                     # AI Backend Service (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   ├── services/
│   │   │   ├── reconstruction.py
│   │   │   ├── anomaly_detection.py
│   │   │   └── llm_agent.py
│   │   └── models/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── models/             # Downloaded ML models
│
├── websocket/              # WebSocket Service (Node.js)
│   ├── src/
│   │   ├── server.js
│   │   ├── handlers/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
│
├── frontend/               # React + Vite Frontend
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── infra/                  # Infrastructure
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── init-scripts/
│
└── README.md
```

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <repo>
cd ai-twin-factory

# 2. Start all services
docker-compose up -d

# 3. Access services
Frontend: http://localhost:5173
API: http://localhost:8001/docs
AI Service: http://localhost:8000/docs
WebSocket: ws://localhost:3000
```

## 📚 Documentation

- [API Service](./api/README.md)
- [AI Service](./ai/README.md)
- [WebSocket Service](./websocket/README.md)
- [Frontend](./frontend/README.md)
