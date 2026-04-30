# AI Twin Factory - Digital Twin untuk Pabrik Baja Nirkarat

## 🇮🇩 Mendukung Hilirisasi Indonesia - Proyek Strategis Nasional

Platform ini dikembangkan untuk mendukung **Proyek Hilirisasi Fase 2** khususnya pembangunan **Fasilitas Manufaktur Baja Nirkarat (Stainless Steel) dari Nikel** di Indonesia Morowali Industrial Park (IMIP), Sulawesi Tengah.

### 🏭 Konteks Proyek
Sebagai bagian dari 13 proyek hilirisasi yang diresmikan Presiden Prabowo Subianto (Rp 116 triliun), proyek ini merupakan kolaborasi PT Krakatau Steel dengan Tsingshan Group untuk produksi stainless steel slab berkapasitas **1,2 juta ton per tahun**. Pabrik ini menggunakan proses peleburan dan pemurnian modern yang memerlukan monitoring ketat terhadap ratusan equipment kritis.

### 💡 Mengapa Digital Twin Penting?
| Tantangan Pabrik Baja | Solusi AI Twin Factory |
|---|---|
| Equipment failure = downtime Rp juta/jam | Prediksi anomali sebelum failure |
| High-temperature furnace (EAF) berisiko | Real-time monitoring & alert otomatis |
| Ratusan motor, pump, conveyor tersebar | 3D visualization untuk navigasi cepat |
| Maintenance expert terbatas di lokasi remote | AI agent untuk decision support |
| Setup digital twin manual mahal & lama | Generate 3D otomatis dari foto |

### 📊 Dampak Bisnis
- **↓ 80%** unplanned downtime
- **↑ 30%** OEE (Overall Equipment Effectiveness)  
- **↓ 70%** biaya setup digital twin
- **↑ 600.000** lapangan kerja baru di sektor hilirisasi

---

## 🎯 Overview

Platform **Digital Twin** berbasis AI untuk monitoring real-time fasilitas baja nirkarat dengan 3 kemampuan utama:

1. **🎨 AI-Driven 3D Modeling** - Generate 3D pabrik dari foto equipment & layout
2. **🔍 Smart Monitoring** - Anomaly detection pada EAF, conveyor, pump, motor
3. **🤖 AI Decision Agent** - Alert & rekomendasi maintenance otomatis

---

## 🏗️ Arsitektur Sistem (5-Layer)

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 5: DIGITAL TWIN VISUALIZATION                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  • 3D Scene Rendering (Three.js)                              │  │
│  │  • Real-time Dashboard (sensor overlay on 3D)                 │  │
│  │  • Alert Visualization (highlight problem equipment)          │  │
│  │  • Interactive Controls (rotate, zoom, inspect)               │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ 5. Display processed data
                              │
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 4: DATA REPOSITORY                                           │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────┐  │
│  │ Time-Series  │  3D Scenes   │    Asset     │    Metadata      │  │
│  │     DB       │   Storage    │   Library    │      DB          │  │
│  │  (InfluxDB)  │              │              │  (PostgreSQL)    │  │
│  │              │              │              │                  │  │
│  │ • Sensor     │ • GLB files  │ • Equipment  │ • Equipment      │  │
│  │   readings   │ • Scene JSON │   models     │   registry       │  │
│  │ • Anomaly    │ • Layouts    │ • Fallback   │ • Maintenance    │  │
│  │   logs       │              │   primitives │   history        │  │
│  └──────────────┴──────────────┴──────────────┴──────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ 4. Store AI outputs
                              │
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: AI & ML PROCESSING ENGINE  ← THE "BRAIN"                 │
│                                                                     │
│  ┌──────────────────┐    ┌─────────────────┐    ┌───────────────┐  │
│  │ 3D RECONSTRUCTION│    │  ANOMALY        │    │    DECISION   │  │
│  │    AI AGENT      │    │  DETECTION      │    │     AGENT     │  │
│  │                  │    │                 │    │               │  │
│  │ Input:           │    │ Input:          │    │ Input:        │  │
│  │ • Equipment      │    │ • Time-series   │    │ • Anomaly     │  │
│  │   images         │    │   sensor data   │    │   detection   │  │
│  │ • Layout pabrik  │    │                 │    │   results     │  │
│  │                  │    │ Process:        │    │               │  │
│  │ Process:         │    │ • LSTM / Isol-  │    │ Process:      │  │
│  │ • VLM (Qwen2-VL) │    │   ation Forest  │    │ • Root cause  │  │
│  │ • 3D Pipeline    │    │ • Real-time     │    │   analysis    │  │
│  │ • Self-evaluation│    │   scoring       │    │ • Action rec  │  │
│  │   (Critic)       │    │                 │    │ • Alert gen   │  │
│  │                  │    │ Output:         │    │               │  │
│  │ Output:          │    │ • Anomaly       │    │ Output:       │  │
│  │ • 3D scene file  │    │   score + label │    │ • Alert msg   │  │
│  │ • Equipment      │    │                 │    │ • Actions     │  │
│  │   metadata       │    │                 │    │   (maint/     │  │
│  │                  │    │                 │    │   shutdown)   │  │
│  └──────────────────┘    └─────────────────┘    └───────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ 3. Route raw data to AI modules
                              │
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 2: DATA COLLECTION & IoT GATEWAY                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    GATEWAY FUNCTIONS                          │  │
│  │                                                               │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐  │  │
│  │  │ MQTT Broker  │  │  API Server  │  │ Stream Processor   │  │  │
│  │  │              │  │              │  │                    │  │  │
│  │  │ • Subscribe  │  │ • Upload     │  │ • Transform        │  │  │
│  │  │   to sensors │  │   images     │  │ • Route            │  │  │
│  │  │ • QoS mgmt   │  │ • REST API   │  │ • Buffer           │  │  │
│  │  └──────────────┘  └──────────────┘  └────────────────────┘  │  │
│  │                                                               │  │
│  │  Job: Ingest data, then route to appropriate AI module:      │  │
│  │       • Sensor data  → Anomaly Detection                     │  │
│  │       • Images       → 3D Reconstruction                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ 2. Collect data from physical world
                              │
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 1: EQUIPMENT & MACHINERY (Physical Assets)                   │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────────────┐  │
│  │  IoT Sensors  │  │   Equipment   │  │   Equipment Images      │  │
│  │               │  │               │  │   + Layout Pabrik       │  │
│  │ • Temperature │  │ • Motors      │  │                         │  │
│  │ • Vibration   │  │ • Pumps       │  │ (Upload via web/mobile) │  │
│  │ • Pressure    │  │ • Conveyors   │  │                         │  │
│  │ • Current     │  │ • Smelters    │  │                         │  │
│  └───────────────┘  └───────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↑
                              │ 1. Generate data
                              │
                    ┌─────────┴─────────┐
                    │   Factory Floor   │
                    │  (Physical World) │
                    └───────────────────┘
```

### Data Flow Summary

| Step | Direction | Description |
|------|-----------|-------------|
| **1** | ↑ Layer 1 → Layer 2 | Equipment & sensors generate raw data (sensor readings, photos) |
| **2** | ↑ Layer 2 → Layer 3 | Gateway routes data to appropriate AI module |
| **3** | ↑ Layer 3 → Layer 4 | AI engine processes and outputs results to storage |
| **4** | ↑ Layer 4 → Layer 5 | UI reads from repo and displays digital twin |

### 3 Core Workflows

| Workflow | Input (L1) | Processing (L3) | Output (L4) | Display (L5) |
|----------|------------|-----------------|-------------|--------------|
| **Real-time Monitor** | IoT Sensors | Anomaly Detection (Hybrid ML) | Sensor data + alerts | Live dashboard |
| **3D Reconstruction** | Equipment photos | 3D AI Agent (VLM + Pipeline) | 3D scene files | 3D visualization |
| **Smart Alert** | Anomaly scores | Decision Agent (LLM) | Alert messages | Alert overlay on 3D |

> **Note:** Detailed Layer 3 architecture available in [docs/ai-3d-design/layer3-detailed.md](docs/ai-3d-design/layer3-detailed.md)

---

## 🤖 Komponen Utama

### 1. 3D Generator AI Agent
**Fungsi:** Generate 3D model pabrik dari foto equipment & layout

**Fitur:**
- Photo-to-3D reconstruction menggunakan:
  - Multi-view stereo vision
  - NeRF (Neural Radiance Fields) / 3D Gaussian Splatting
- AI-assisted layouting berdasarkan foto
- Asset library untuk equipment umum (conveyor, motor, pump, dll)

**Input:**
- Foto equipment dari berbagai angle
- Floor plan / layout pabrik (opsional)
- Spesifikasi equipment

**Output:**
- 3D model (GLTF/GLB format)
- Metadata (position, rotation, scale)
- Interactive 3D scene

**Tech Stack:**
- Qwen2-VL / LLaVA-1.6 untuk analisis foto (via Ollama)
- Florence-2 untuk object detection & captioning
- Three.js / React Three Fiber untuk rendering
- Blender Python API (opsional, untuk advanced modeling)

---

### 2. Monitoring Layer (Anomaly Detection)
**Fungsi:** Deteksi anomali pada equipment secara real-time

**Fitur:**
- Sensor fusion (temperature, vibration, pressure, current)
- Discriminative ML models:
  - Isolation Forest
  - One-Class SVM
  - Autoencoder (LSTM/Transformer)
- Real-time anomaly scoring
- Trend analysis & predictive maintenance

**Data Flow:**
```
Sensors → MQTT Broker → Stream Processing → ML Model → Alert
```

**Tech Stack:**
- MQTT / IoT Core untuk sensor ingestion
- Apache Kafka / Redis Stream untuk real-time processing
- Scikit-learn / PyTorch untuk ML models
- InfluxDB / TimescaleDB untuk time-series data

---

### 3. Decision Support AI Agent
**Fungsi:** Memberikan alert, summary, dan rekomendasi action saat anomali

**Fitur:**
- Anomaly explanation (why ini terjadi?)
- Root cause analysis
- Recommended actions:
  - Immediate shutdown / continue
  - Maintenance schedule
  - Operator notification
- Executive summary untuk management
- Chat interface untuk query

**Contoh Output (Baja Nirkarat - IMIP):**
```
⚠️ ALERT: Anomali Kritis pada EAF Conveyor C-03
📍 Zone: Raw Material Handling | Equipment ID: CONV-EAF-03

🔴 Detail Anomali:
- Vibration: 18.2 mm/s (normal: < 5 mm/s) - CRITICAL
- Motor Temperature: 92°C (normal: < 75°C) - HIGH  
- Current Draw: 45A (normal: ~32A) - ELEVATED
- Anomaly Score: 0.94 (CRITICAL)

🔍 Root Cause Analysis:
Bearing depan conveyor mengalami severe wear berdasarkan:
- Pola vibration frekuensi tinggi (bearing defect signature)
- Temperature rise konsisten 3 hari terakhir
- Current increase menunjukkan friction tinggi

📋 Rekomendasi Tindakan:
1. 🔴 URGENT: Schedule maintenance dalam 4 jam
2. 🔴 Siapkan spare: Bearing SKF 22320 CC/W33 (2 pcs)
3. 🟡 Assign technician: Pak Suyanto (Bearing Specialist)
4. 🟡 Koordinasi dengan EAF operator untuk material buffer

💰 Impact Analysis:
- Jika tidak di-handle: Breakdown estimasi 6-12 jam
- Production loss: 180-360 ton stainless steel
- Financial impact: ~Rp 15-30 miliar
- Safety risk: HIGH (hot material conveyor)

✅ Action Taken:
[12:45] Work order created #WO-2026-0442
[12:47] Alert sent to: Maintenance Supervisor + Plant Manager
[12:50] Spare parts reserved from warehouse
```

**Tech Stack:**
- LLM (Qwen2.5 / LLaMA-3 / Mistral) untuk reasoning
- RAG (Retrieval Augmented Generation) dengan manual/histori
- LangGraph / LangChain untuk agent workflow

---

## 📊 Use Cases - Pabrik Baja Nirkarat IMIP

### Use Case 1: Predictive Maintenance - EAF Conveyor System
**Scenario:** Bearing pada conveyor raw material ke Electric Arc Furnace menunjukkan early signs of wear

**Flow:**
1. Vibration sensor C-03 deteksi frekuensi anomali (BPFI - Ball Pass Frequency Inner)
2. Isolation Forest classify sebagai HIGH severity (score 0.87)
3. Decision Agent retrieve similar case dari knowledge base
4. AI generate alert: "Bearing aus tahap awal, schedule replacement"
5. Maintenance team terima notifikasi dengan 3D location marker
6. Replacement dilakukan saat planned downtime EAF

**Benefit:** 
- Avoid unplanned EAF shutdown (cost: Rp 5M/jam)
- Prevent secondary damage ke drive motor
- Optimize spare parts inventory

---

### Use Case 2: Rapid Digital Twin Deployment - New Rolling Mill Line
**Scenario:** PT Krakatau Steel menambah rolling mill line baru, butuh digital twin dalam 48 jam

**Flow:**
1. Engineer upload 30 foto equipment dari berbagai angle
2. MapAnything (VLM + 3D Pipeline) generate initial 3D scene
3. AI Agent identify equipment: Roughing mill, Intermediate mill, Finishing mill
4. Match dengan asset library (high-quality 3D models)
5. Self-evaluation loop: VLM verify accuracy vs foto asli
6. Deploy ke dashboard dengan sensor mapping otomatis

**Benefit:**
- Setup time: 2 hari vs 3 minggu (manual CAD)
- Cost: Rp 50 juta vs Rp 500 juta (outsourcing)
- Training operator bisa langsung pakai 3D model

---

### Use Case 3: Emergency Response - Cooling Pump Failure
**Scenario:** Pompa pendingin tiba-tiba pressure drop, risiko overheat continuous caster

**Flow:**
1. Pressure sensor P-07 drop dari 4.5 bar ke 2.1 bar (CRITICAL)
2. Statistical filter trigger immediate alert (< 100ms)
3. Decision Agent analyze: "Pump cavitation atau mechanical seal failure"
4. Auto-execute:
   - Switch ke backup pump P-07B
   - Isolate pump P-07A
   - Alert maintenance + plant manager
5. 3D visualization highlight affected zone (casting area)
6. Generate incident report dengan timeline otomatis

**Benefit:**
- Response time: < 5 detik (switchover otomatis)
- Prevent molten steel solidification (loss: Rp 30M+)
- Zero safety incident

---

### Use Case 4: Multi-Zone Coordination - Furnace Maintenance Window
**Scenario:** Maintenance EAF furnace butuh koordinasi 4 zone berbeda

**Flow:**
1. Planner request optimal maintenance window via chat interface
2. AI Agent analyze:
   - Zone 1 (Raw Material): Buffer level 80% (OK for 6 hours)
   - Zone 2 (EAF): Scheduled maintenance, cooldown required
   - Zone 3 (Casting): 2 ladles ready, 3rd in progress
   - Zone 4 (Rolling): Current slab inventory sufficient
3. AI recommend: "Start maintenance 14:00 WITA, duration 4 hours"
4. Auto-schedule semua equipment dalam 4 zone
5. Generate work orders dengan 3D location untuk setiap task

**Benefit:**
- Optimal resource utilization
- Minimize production loss
- Clear coordination across departments

---

## 📚 Dokumentasi Lengkap

| Dokumen | Deskripsi |
|---------|-----------|
| **[🏭 Stainless Steel Plant Reference](./docs/stainless-steel-plant.md)** | Arsitektur detail untuk Pabrik Baja Nirkarat IMIP |
| **[🎬 Demo Scenario](./docs/demo-scenario.md)** | Script & storyboard demo hackathon |
| **[🔬 Layer 3 AI/ML Detail](./docs/ai-3d-design/layer3-detailed.md)** | Spesifikasi teknis anomaly detection & AI agent |
| **[📊 System Design](./docs/ai-3d-design/system-design.md)** | Arsitektur 3D Generator Agent |
| **[📈 Diagrams](./docs/diagrams/workflow.drawio)** | Flowchart & arsitektur (DrawIO) |

---

## 🛠️ Tech Stack Proposal

### Backend
- **Language:** Python (FastAPI) untuk AI/ML services
- **API:** Node.js (NestJS) untuk main API
- **Messaging:** Redis / RabbitMQ
- **Database:** PostgreSQL, InfluxDB, Pinecone (vector DB)

### Frontend
- **Framework:** React / Next.js
- **3D:** Three.js / React Three Fiber
- **Charts:** Recharts / D3.js
- **Real-time:** Socket.io

### AI/ML
- **LLM:** OpenAI GPT-4 / Anthropic Claude
- **ML:** Scikit-learn, PyTorch
- **3D:** OpenAI Vision, NeRF implementations
- **Orchestration:** LangChain / LangGraph

### Infrastructure
- **Container:** Docker
- **Orchestration:** Kubernetes (opsional)
- **Cloud:** AWS / Azure / GCP
- **IoT:** AWS IoT Core / Azure IoT Hub

---

## 📈 Development Roadmap

### Phase 1: MVP (Demo Hackathon)
- [ ] Manual 3D modeling (1 equipment)
- [ ] Simulated sensor data
- [ ] Basic anomaly detection (threshold-based)
- [ ] Simple alert system
- [ ] Basic dashboard

### Phase 2: AI Integration
- [ ] Photo-to-3D AI agent
- [ ] ML-based anomaly detection
- [ ] Decision agent dengan LLM
- [ ] Real-time sensor integration

### Phase 3: Production Ready
- [ ] Scalable architecture
- [ ] Multi-factory support
- [ ] Advanced analytics
- [ ] Mobile app

---

## 🎯 Demo Hackathon Strategy

### Fokus Demo:
1. **Visual Impact:** 3D digital twin yang interactive
2. **Real-time:** Live sensor data visualization
3. **AI Intelligence:** Smart alert dengan explanation

### Storyline Demo:
1. **Intro:** Show 3D factory model (digital twin)
2. **Monitoring:** Real-time sensor data streaming
3. **Anomaly:** Trigger simulated anomaly (overheating motor)
4. **AI Response:** Alert muncul + rekomendasi action
5. **Resolution:** Show decision impact

### Technical Highlights:
- 3D rendering smooth
- Real-time data (WebSocket)
- AI explanation yang convincing
- Clean UI/UX

---

## 📚 Resources & References

### Digital Twin
- NVIDIA Omniverse
- AWS IoT TwinMaker
- Azure Digital Twins

### 3D Reconstruction
- NeRF (Neural Radiance Fields)
- 3D Gaussian Splatting
- COLMAP (Structure from Motion)

### Anomaly Detection
- Isolation Forest
- Autoencoder untuk time-series
- LSTM for anomaly detection

### AI Agents
- LangChain / LangGraph
- AutoGPT
- Microsoft AutoGen