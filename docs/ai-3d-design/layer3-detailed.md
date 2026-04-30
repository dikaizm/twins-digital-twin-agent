# Layer 3 Detailed Architecture

## 3.1 Anomaly Detection Pipeline (Hybrid Approach)

**Why hybrid?** Different anomalies require different detection methods.

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ANOMALY DETECTION PIPELINE                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Stage 1: Statistical Filter (Real-time, <100ms)                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Z-score > 3? → CRITICAL alert                              │   │
│  │ • Threshold: temp > 100°C, vibration > 10mm/s                │   │
│  │ • Action: Instant alert, bypass ML                           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Stage 2: Isolation Forest (Every 30s, batch)                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Input: Multi-sensor vector [temp, vibration, pressure,      │   │
│  │                             current, power]                  │   │
│  │                                                              │   │
│  │ Algorithm: Isolation Forest (unsupervised)                   │   │
│  │ • Contamination: 0.05 (5% expected anomalies)                │   │
│  │ • Trees: 100                                                 │   │
│  │ • Output: Anomaly score 0.0-1.0                              │   │
│  │ • Feature importance: Which sensor contributes most?         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Stage 3: LSTM Autoencoder (Optional, offline training)             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ For: Gradual degradation patterns (bearing wear, etc.)       │   │
│  │                                                              │   │
│  │ Architecture:                                                  │   │
│  │ • Input: 50 timesteps × 4 sensors                            │   │
│  │ • Encoder: LSTM(64) → LSTM(32)                               │   │
│  │ • Decoder: LSTM(32) → LSTM(64) → Dense(4)                    │   │
│  │ • Loss: MSE reconstruction error                             │   │
│  │ • Threshold: error > μ + 3σ                                  │   │
│  │                                                              │   │
│  │ Training: Unsupervised (train only on "normal" data)         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Algorithm Selection Rationale:**

| Method | Use Case | Latency | Data Required | Interpretability |
|--------|----------|---------|---------------|------------------|
| **Z-score** | Critical thresholds | <10ms | None | High |
| **Isolation Forest** | Multi-variate anomalies | 100ms | 1000+ samples | Medium |
| **LSTM Autoencoder** | Temporal degradation | 500ms | 10k+ sequences | Low |

---

## 3.2 AI Decision Agent (LLM-based)

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────┐
│                    AI DECISION AGENT                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Input Context Builder                                          │ │
│  │  • Anomaly detection result (score, severity)                  │ │
│  │  • Sensor values (current vs normal range)                     │ │
│  │  • Equipment metadata (type, age, maintenance history)         │ │
│  │  • 3D scene context (position, surrounding equipment)          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  LLM Core (via API)                                             │ │
│  │                                                                 │ │
│  │  Options for Hackathon:                                         │ │
│  │  A. Qwen2.5-14B (local via Ollama) - FREE, private             │ │
│  │  B. OpenRouter API (Qwen/DeepSeek) - $0.001-0.003/1K tokens    │ │
│  │  C. Groq API (LLaMA-3) - Fast, $0.0005/1K tokens               │ │
│  │                                                                 │ │
│  │  Prompt Strategy:                                               │ │
│  │  - System prompt: "You are an expert maintenance engineer"     │ │
│  │  - Few-shot examples for consistent output format              │ │
│  │  - Structured output: JSON with severity, actions, impact      │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  RAG Knowledge Base (Retrieval Augmented Generation)            │ │
│  │                                                                 │ │
│  │  Vector DB contains:                                            │ │
│  │  • Equipment manuals (embedded text chunks)                    │ │
│  │  • Historical maintenance logs                                 │ │
│  │  • Similar past incidents with resolutions                     │ │
│  │  • Safety procedures & SOPs                                    │ │
│  │                                                                 │ │
│  │  Retrieval: Top-3 relevant chunks added to context             │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Tool Calling (Function Calling)                                │ │
│  │                                                                 │ │
│  │  Available Tools:                                               │ │
│  │  1. schedule_maintenance(equipment_id, priority, timeframe)    │ │
│  │  2. send_alert_email(recipients[], subject, body, severity)    │ │
│  │  3. shutdown_equipment(equipment_id, reason) - CRITICAL only   │ │
│  │  4. query_equipment_specs(equipment_id) → return manual info   │ │
│  │  5. create_work_order(equipment_id, description, assignee)     │ │
│  │                                                                 │ │
│  │  Auto-execute if: confidence > 0.9 AND severity == CRITICAL    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Output Format (Structured JSON)                                │ │
│  │  {                                                              │ │
│  │    "summary": "Motor-01 showing high vibration",               │ │
│  │    "severity": "HIGH",                                          │ │
│  │    "root_cause_hypothesis": "Bearing wear based on pattern",   │ │
│  │    "confidence": 0.87,                                          │ │
│  │    "actions": [                                                 │ │
│  │      {                                                          │ │
│  │        "type": "schedule_maintenance",                         │ │
│  │        "priority": "HIGH",                                      │ │
│  │        "timeframe": "within 24 hours",                         │ │
│  │        "auto_execute": false,                                   │ │
│  │        "reason": "Prevent catastrophic failure"                │ │
│  │      },                                                         │ │
│  │      {                                                          │ │
│  │        "type": "send_alert_email",                             │ │
│  │        "recipients": ["supervisor@factory.com"],               │ │
│  │        "auto_execute": true                                     │ │
│  │      }                                                          │ │
│  │    ],                                                           │ │
│  │    "impact_if_ignored": "Estimated 2-3 days downtime, $50k loss"│ │
│  │  }                                                              │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Severity Levels & Thresholds:**

| Severity | Anomaly Score | Response Time | Auto-Action | Human Approval |
|----------|--------------|---------------|-------------|----------------|
| **CRITICAL** | > 0.9 | Immediate | Shutdown + Alert | Notification only |
| **HIGH** | 0.8 - 0.9 | < 5 min | Alert + Suggest | Required for action |
| **MEDIUM** | 0.6 - 0.8 | < 30 min | Log + Monitor | Optional |
| **LOW** | 0.5 - 0.6 | < 2 hours | Log only | N/A |

---

## 3.3 3D Reconstruction AI Pipeline

**Sub-modules:**

```
┌──────────────────────────────────────────────────────────────────────┐
│              3D RECONSTRUCTION PIPELINE                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Module 1: Vision Understanding (Qwen2-VL / LLaVA-1.6)              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Input: Equipment photos (multiple angles)                    │   │
│  │                                                              │   │
│  │ VLM Tasks:                                                   │   │
│  │ • "Identify all equipment in this image"                     │   │
│  │ • "Estimate relative positions"                              │   │
│  │ • "Classify equipment type: motor/pump/conveyor/etc"         │   │
│  │                                                              │   │
│  │ Output: Equipment list with:                                 │   │
│  │ • name, type, confidence, bounding_box                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Module 2: Asset Matching (Vector DB + CLIP embeddings)             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ For each detected equipment:                                 │   │
│  │                                                              │   │
│  │ 1. Generate CLIP embedding dari nama + deskripsi VLM        │   │
│  │ 2. Search di Vector DB (cosine similarity)                  │   │
│  │ 3. If similarity > 0.8: Use existing 3D model              │   │
│  │ 4. Else: Use procedural primitive (box/cylinder)            │   │
│  │                                                              │   │
│  │ Asset Library Structure:                                     │   │
│  │ /assets/                                                     │   │
│  │   ├── motor/                                                 │   │
│  │   │   ├── motor_5hp.glb + metadata.json                     │   │
│  │   │   └── motor_10hp.glb + metadata.json                    │   │
│  │   ├── pump/                                                  │   │
│  │   └── conveyor/                                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Module 3: Layout Solver (Constraint-based optimization)            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Input: Equipment list + estimated positions + floor plan     │   │
│  │                                                              │   │
│  │ Constraints:                                                 │   │
│  │ • Safety distance (min 1m between equipment)                 │   │
│  │ • Material flow (conveyor input → output alignment)          │   │
│  │ • Floor plan boundaries                                      │   │
│  │ • Maintenance access (min 0.5m clearance)                    │   │
│  │                                                              │   │
│  │ Algorithm: Simulated Annealing                               │   │
│  │ • Optimize: minimize constraint violations                   │   │
│  │ • Output: Final (x, y, z) for each equipment                │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Module 4: Scene Assembly (Three.js + GLTF export)                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Load matched 3D assets                                     │   │
│  │ • Apply transforms (position, rotation, scale)               │   │
│  │ • Add lighting (ambient + directional)                       │   │
│  │ • Add ground plane                                           │   │
│  │ • Export: GLB file + JSON metadata                           │   │
│  │                                                              │   │
│  │ Metadata JSON:                                               │   │
│  │ {                                                            │   │
│  │   "scene_id": "factory_01",                                  │   │
│  │   "equipment": [                                             │   │
│  │     {                                                        │   │
│  │       "id": "motor_01",                                      │   │
│  │       "type": "motor",                                       │   │
│  │       "position": [x, y, z],                                 │   │
│  │       "rotation": [rx, ry, rz],                              │   │
│  │       "asset_path": "assets/motor/motor_5hp.glb",            │   │
│  │       "sensor_mapping": {                                    │   │
│  │         "temp_sensor_01": "sensor_id_123"                    │   │
│  │       }                                                      │   │
│  │     }                                                        │   │
│  │   ]                                                          │   │
│  │ }                                                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              ↓                                       │
│  Module 5: Self-Evaluation (Critic Loop)                            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Render 4 angles dari 3D scene                             │   │
│  │ • VLM compare: "Does this match original photos?"           │   │
│  │ • Score: accuracy, layout, completeness, proportion         │   │
│  │ • If score < 0.8: Generate fix plan → re-run modules        │   │
│  │ • Max 3 retries                                             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3.4 Integration: Anomaly Detection → AI Agent

```
┌──────────────────────────────────────────────────────────────────────┐
│              DETECTION → DECISION INTEGRATION                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐                                                │
│  │ Anomaly Detection│                                                │
│  │ Pipeline         │                                                │
│  └────────┬─────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Decision Router (Threshold-based)                           │   │
│  │                                                              │   │
│  │  IF score > 0.9:        → LLM Agent (CRITICAL context)       │   │
│  │  ELSE IF score > 0.7:   → LLM Agent (HIGH context)           │   │
│  │  ELSE IF score > 0.5:   → LLM Agent (MEDIUM context)         │   │
│  │  ELSE:                  → Log only (no LLM call)             │   │
│  │                                                              │   │
│  │  Context enrichment:                                         │   │
│  │  • Add similar past incidents from RAG                       │   │
│  │  • Add equipment manual excerpts                             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│           │                                                          │
│           ▼                                                          │
│  ┌──────────────────┐                                                │
│  │   LLM Agent      │                                                │
│  │   (if routed)    │                                                │
│  └────────┬─────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Tool Execution                                              │   │
│  │                                                              │   │
│  │  Auto-execute (if confidence > 0.9 AND severity = CRITICAL): │   │
│  │    • shutdown_equipment()                                    │   │
│  │    • send_alert_email()                                      │   │
│  │                                                              │   │
│  │  Human approval required:                                    │   │
│  │    • schedule_maintenance()                                  │   │
│  │    • create_work_order()                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3.5 Technology Stack for Layer 3

| Component | Technology | Reasoning |
|-----------|------------|-----------|
| **Anomaly Detection** | Python + scikit-learn (Isolation Forest) + PyTorch (LSTM) | Mature, well-documented, fast inference |
| **LLM for Agent** | Qwen2.5-14B via Ollama (local) | FREE, no API limits, data privacy |
| **Alternative LLM** | Groq API (LLaMA-3-70B) | Fastest inference (800 tokens/s), cheap |
| **Vector DB (RAG)** | ChromaDB or pgvector | Simple, integrates with LangChain |
| **Embeddings** | BGE-M3 or E5 (multilingual) | Good for Indonesian equipment manuals |
| **Agent Framework** | LangGraph | State management, conditional edges, visualization |
| **VLM for 3D** | Qwen2-VL-7B via Ollama | Open source, handles Indonesian context |
| **3D Processing** | Three.js + GLTF | Browser-native, efficient, widely supported |
| **Asset Matching** | CLIP (OpenAI) or EVA-CLIP | Vision-language embeddings for equipment |
