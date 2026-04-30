# AI 3D Generator Agent — System Design

## 🇮🇩 Strategic Context: Hilirisasi Manufacturing

Platform ini adalah **enabler digital** untuk program hilirisasi industri Indonesia. Dengan mempercepat dan murahnya deployment digital twin, pabrik-pabrik hilirisasi (smelter nikel, pengolahan bauksit, CPO refinery, dll) dapat:

1. **Standarisasi operasi** — semua pabrik punya baseline digital
2. **Transfer expertise** — knowledge engineer/manufacturing expert didistribusikan via AI
3. **Optimasi berkelanjutan** — data-driven decision making
4. **Skalabilitas** — dari 1 lini ke seluruh kawasan industri

> **"Make Indonesia's downstream factories world-class through AI-powered digital twin."**

## Overview

Agent yang bertugas mengubah foto equipment/layout pabrik menjadi 3D digital twin secara (semi-)otomatis. Bukan pure AI generating mesh dari nol, tapi hybrid approach: **computer vision + photogrammetry + intelligent asset assembly**.

---

## High-Level Architecture

```
                          ┌─────────────────────────┐
                          │      User Upload         │
                          │  (Foto equipment,        │
                          │   floor plan, specs)     │
                          └──────────┬──────────────┘
                                     │
                          ┌──────────▼──────────────┐
                          │   Orchestrator Agent     │
                          │  (langgraph workflow)    │
                          └──┬───────────┬─────────┘
                             │           │
                    ┌────────▼──┐  ┌─────▼──────────┐
                    │ Vision    │  │ Factory Layout  │
                    │ Pipeline  │  │ Agent           │
                    └────┬──────┘  └────┬───────────┘
                         │              │
           ┌─────────────┼──────┬───────┼──────────────┐
           │             │      │       │              │
    ┌──────▼──────┐ ┌───▼──┐ ┌─▼───┐ ┌▼───────┐  ┌───▼────┐
    │ Object      │ │Pose  │ │Size │ │Asset  │  │Floor   │
    │Detection    │ │Estim.│ │Estim│ │Library│  │Planner │
    └──────┬──────┘ └──┬───┘ └──┬──┘ └───┬───┘  └───┬────┘
           │           │        │        │           │
           └───────────┼────────┼────────┼───────────┘
                       │        │        │
                ┌──────▼────────▼────────▼──────────┐
                │        3D Scene Assembler          │
                │  (positioning, scaling, lighting)  │
                └────────────────┬──────────────────┘
                                 │
                ┌────────────────▼──────────────────┐
                │              Critic                │
                │        (Self-Evaluation Node)      │
                │  ┌──────────────────────────┐     │
                │  │ Render 2D preview         │     │
                │  │ VLM: compare vs original  │     │
                │  │ photos                     │     │
                │  │ Score: accuracy, layout,   │     │
                │  │ completeness, visual       │     │
                │  └──────────┬───────────────┘     │
                └─────────────┬────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Score ≥ 0.8?   │
                    └───┬────────┬───┘
                   NO   │        │  YES
               ┌────────▼──┐     │
               │ Feedback   │     │
               │ Generator   │     │
               │ (specific   │     │
               │  fix        │     │
               │  instruction)│    │
               └──┬─────────┘     │
          ┌───────┼───────────────┼──────────┐
          │       │  max_retry?   │          │
          │  ┌────▼────┐         │          │
          │  │ Re-run   │         │          │
          │  │ pipeline │         │          │
          │  │ (targeted│         │          │
          │  │ fix)     │         │          │
          │  └─────────┘         │          │
          └──────────────────────┘          │
                               ┌────────────▼──────────┐
                               │   Final 3D Scene       │
                               │   + Evaluation Report  │
                               │   Digital Twin         │
                               └────────────────────────┘
```

---

## Agent Workflow (LangGraph)

```
State:
  - uploaded_photos: list[Photo]
  - equipment_list: list[Equipment]
  - detected_objects: list[DetectedObject]
  - scene_metadata: SceneLayout
  - evaluation_score: float | None
  - evaluation_report: dict | None
  - critique_feedback: str | None
  - retry_count: int = 0
  - max_retries: int = 3
  - user_feedback: str | None

Nodes:
  1. extract_equipment()
     - VLM: "Apa saja equipment di foto ini?"
     - Output: [{name, type, confidence, bounding_box}]

  2. estimate_pose_size()
     - Classical CV + heuristics
     - Output: {position, rotation, dimensions}

  3. match_or_generate_asset()
     - Cari asset di library
     - Jika tidak ada: trigger photogrammetry pipeline
     - Fallback: procedural primitives + text description
     - Output: {model_path, asset_metadata}

  4. resolve_layout()
     - Floor plan analysis (jika ada)
     - Constraint-based layouting
     - Output: SceneLayout {equipment_positions[]}

  5. assemble_scene()
     - Load semua asset
     - Apply transform
     - Lighting & environment
     - Output: 3D scene file

  6. evaluate_scene()                     ← NEW: Self-Evaluation
     - Render preview dari 3D scene
     - VLM bandingkan dengan foto asli
     - Score 4 dimensi (lihat scoring matrix)
     - Output: {score, report, passed}

  7. generate_feedback()                  ← NEW: Critique Generator
     - Jika score < threshold:
       - Analisis kelemahan spesifik
       - Generate targeted fix instruction
     - Output: {feedback, fix_plan}

  8. apply_fixes()                        ← NEW: Self-Correction
     - Parse fix_plan
     - Re-run pipeline nodes yang relevan
     - Target: hanya bagian yang error
     - Output: updated scene

  9. review_with_user()
     - Render preview final
     - Tampilkan evaluation report
     - Feedback loop
     - Output: approved | revision_request

Edges:
  extract_equipment → estimate_pose_size
  estimate_pose_size → match_or_generate_asset
  match_or_generate_asset → resolve_layout
  resolve_layout → assemble_scene
  assemble_scene → evaluate_scene
  evaluate_scene → generate_feedback (if score < threshold && retry < max_retries)
  evaluate_scene → review_with_user (if score >= threshold)
  evaluate_scene → review_with_user (if retry >= max_retries, with fallback note)
  generate_feedback → apply_fixes
  apply_fixes → assemble_scene (re-entry)
  review_with_user → extract_equipment (if revision)
  review_with_user → END (if approved)
```

---

## Component Deep Dive

### 1. Vision Pipeline

| Sub-component | Teknologi | Output |
|---|---|---|
| Object Detection | YOLOv8 / Grounding DINO | bounding boxes, class labels |
| Visual QA | Qwen2-VL / LLaVA-1.6 / InternVL2 | equipment identification, spesifikasi |
| Pose Estimation | PnP + COLMAP sparse | 6-DOF pose |
| Size Estimation | Reference object + depth | approximate dimensions |

**Flow:**
```
Raw Image → YOLO detect → crop per object → Qwen2-VL / LLaVA identify → 
COLMAP feature matching → PnP pose → size from reference scale
```

### 2. Asset Library

```
assets/
├── conveyor/
│   ├── conveyor_belt_1m.glb
│   ├── conveyor_belt_2m.glb
│   └── conveyor_belt_curved.glb
├── motor/
│   ├── motor_5hp.glb
│   └── motor_10hp.glb
├── pump/
│   ├── centrifugal_pump.glb
│   └── piston_pump.glb
├── robot_arm/
│   ├── 6axis_arm.glb
│   └── 4axis_arm.glb
└── generic/
    ├── tank_cylindrical.glb
    └── tank_rectangular.glb
```

**Strategi matching:**
- Vision → deskripsi equipment → embedding cari similarity di vector DB
- Cocokkan metadata (name, dimensions, type)
- Fallback: procedural generation (Three.js primitives)

### 3. Photogrammetry Pipeline (Custom Parts)

```
Foto multi-angle → COLMAP feature extraction → 
Sparse reconstruction → MVS dense cloud → 
Poisson surface reconstruction → Simplify → GLTF export
```

**Trade-off:** Akurat tapi lambat. Untuk hackathon: **skip atau fallback.**

### 4. Factory Layout Agent

```
Input: Floor plan image, detected equipment list
Process:
  1. OCR + CV untuk ekstrak dimensi ruangan
  2. Grid-based layout optimization
  3. Constraint satisfaction:
     - Jarak antar equipment
     - Safety zone
     - Material flow
  4. Generate candidate layouts
  5. User pilih atau edit
```

**Algoritma:** 
- Layout sebagai 2D bin packing problem
- Heuristic: Best Fit Decreasing + simulated annealing
- LLM untuk interpretasi floor plan image

### 5. Scene Assembler

```
for equipment in equipment_list:
    asset = load_model(equipment.asset_path)
    asset.position = equipment.position
    asset.rotation = equipment.rotation
    asset.scale = equipment.dimensions / asset.default_dimensions
    
    # Add metadata
    asset.userData = {
        id: equipment.id,
        name: equipment.name,
        sensor_data: { temp: null, vibration: null }
    }
    
    scene.add(asset)

# Environment
scene.add(ground_plane)
scene.add(ambient_light)
scene.add(area_lights at equipment positions)

export(scene, format="glb")
export_metadata(scene, format="json")
```

---

### 6. Self-Evaluation & Correction Loop

**Tujuan:** Agent mengevaluasi hasil generate-nya sendiri secara objektif menggunakan VLM, lalu memperbaiki secara otonom sebelum menampilkan ke user.

#### Evaluation Protocol

```
┌─────────────────────────────────────────────────────┐
│                   EVALUATION                          │
├─────────────────────────────────────────────────────┤
│                                                       │
│   Step 1: Render Preview                              │
│   → Render 3D scene dari 4 angle (front, side,        │
│     top, isometric)                                   │
│   → Export sebagai image grid                          │
│                                                       │
│   Step 2: VLM Comparison                              │
│   Prompt ke VLM:                                       │
│     "Bandingkan render 3D ini dengan foto asli.       │
│      Beri score 0.0-1.0 untuk setiap kategori:        │
│      - accuracy: apakah equipment bentuknya sesuai?    │
│      - layout: apakah posisi equipment benar?          │
│      - completeness: apakah semua equipment ada?       │
│      - proportion: apakah skala/ukuran proporsional?   │
│      - visual_quality: apakah pencahayaan realistik?"  │
│                                                       │
│   Step 3: Scoring                                     │
│   Weighted average:                                    │
│     total = accuracy(0.35) + layout(0.25)             │
│           + completeness(0.20) + proportion(0.15)      │
│           + visual_quality(0.05)                       │
│   Threshold: 0.8                                       │
│                                                       │
└─────────────────────────────────────────────────────┘
```

#### Scoring Matrix Detail

| Dimension | Weight | What It Measures | VLM Prompt Template |
|---|---|---|---|
| `accuracy` | 0.35 | Apakah 3D model mirip equipment asli? | "Apakah bentuk, detail utama, dan proporsi equipment di 3D sesuai dengan foto?" |
| `layout` | 0.25 | Apakah posisi & orientasi benar? | "Apakah posisi setiap equipment di 3D sesuai dengan layout di foto?" |
| `completeness` | 0.20 | Apakah semua equipment ter-render? | "Apakah semua equipment yang ada di foto muncul di 3D scene?" |
| `proportion` | 0.15 | Apakah skala relatif benar? | "Apakah ukuran relatif antar equipment proporsional?" |
| `visual_quality` | 0.05 | Apakah render visually acceptable? | "Apakah pencahayaan dan material cukup realistis?" |

#### Self-Correction Strategy

```
Score < 0.8:
  ↓
VLM generates structured feedback:
  {
    "issues": [
      {
        "type": "missing_equipment",
        "target": "pump_02",
        "description": "Pump centrifugal tidak muncul di scene",
        "severity": "high",
        "fix": "add_asset_to_scene"
      },
      {
        "type": "wrong_position",
        "target": "motor_01",
        "description": "Motor terlalu ke kiri 2 meter",
        "severity": "medium",
        "fix": "adjust_position(x=4.5, z=2.0)"
      },
      {
        "type": "wrong_asset",
        "target": "conveyor_01",
        "description": "Conveyor belt lurus, harusnya curved",
        "severity": "high",
        "fix": "replace_asset(conveyor_curved.glb)"
      }
    ],
    "score_breakdown": {
      "accuracy": 0.65,
      "layout": 0.72,
      "completeness": 0.55,
      "proportion": 0.80,
      "visual_quality": 0.90
    }
  }
  ↓
Parsing → Target specific fix per issue:
  - missing_equipment → re-run match_or_generate + assemble
  - wrong_position → re-run resolve_layout (override)
  - wrong_asset → re-run match_or_generate (override type)
  ↓
Apply fix → reassemble → re-evaluate
  ↓
max 3 retries. Jika masih < 0.8 → tampilkan ke user
  dengan catatan "perlu review manual"
```

#### Implementation Detail

```python
class SceneCritic:
    """Self-evaluation node untuk 3D scene generation."""

    def __init__(self, vlm_model: str = "qwen2-vl-7b"):
        self.vlm = load_vlm(vlm_model)
        self.threshold = 0.8
        self.max_retries = 3
        self.dimensions = {
            "accuracy": 0.35,
            "layout": 0.25,
            "completeness": 0.20,
            "proportion": 0.15,
            "visual_quality": 0.05,
        }

    async def evaluate(self, scene: Scene3D, photos: list[Image]) -> EvaluationResult:
        previews = await self.render_previews(scene)
        prompt = self.build_evaluation_prompt(previews, photos)
        response = await self.vlm.generate(prompt)
        scores = self.parse_scores(response)
        total = self.weighted_score(scores)
        issues = self.parse_issues(response)

        return EvaluationResult(
            score=total,
            scores_per_dimension=scores,
            issues=issues,
            passed=total >= self.threshold,
        )

    async def generate_fix_plan(self, result: EvaluationResult) -> list[FixInstruction]:
        prompt = f"""
        Scene evaluation result:
        - Score: {result.score}
        - Issues: {result.issues}

        Generate specific fix instructions.
        For each issue, specify:
        1. Which pipeline node to re-run
        2. What override parameters to use
        3. Priority order
        """
        response = await self.vlm.generate(prompt)
        return self.parse_fix_instructions(response)

    async def apply_fixes(self, scene: Scene3D, fixes: list[FixInstruction]) -> Scene3D:
        for fix in fixes:
            if fix.type == "missing_equipment":
                asset = await self.asset_library.match(fix.target_equipment)
                scene.add_equipment(asset, fix.position)
            elif fix.type == "wrong_position":
                scene.move_equipment(fix.target, fix.new_position)
            elif fix.type == "wrong_asset":
                new_asset = await self.asset_library.match(fix.correct_type)
                scene.replace_equipment(fix.target, new_asset)
        return scene

    def weighted_score(self, scores: dict[str, float]) -> float:
        total = 0.0
        for dim, weight in self.dimensions.items():
            total += scores.get(dim, 0.0) * weight
        return round(total, 2)

    def build_evaluation_prompt(self, previews: list[Image], photos: list[Image]) -> str:
        return f"""
        Berikut adalah foto asli pabrik dan render 3D hasil generate.
        Evaluasi kualitas render 3D berdasarkan kriteria berikut:

        Foto asli: {len(photos)} image(s)
        Render 3D preview: {len(previews)} angle(s)

        Evaluasi setiap dimensi dengan score 0.0 - 1.0:
        - accuracy: Apakah bentuk equipment sesuai dengan foto asli?
        - layout: Apakah posisi dan orientasi equipment sesuai layout?
        - completeness: Apakah semua equipment ter-render semua?
        - proportion: Apakah skala dan ukuran proporsional?
        - visual_quality: Apakah lighting dan material baik?

        Jika ada masalah, sebutkan detail issue-nya:
        - Equipment mana yang bermasalah?
        - Apa masalahnya (missing, wrong position, wrong shape)?
        - Severity (high/medium/low)

        Format response:
        ```json
        {{
            "accuracy": 0.85,
            "layout": 0.70,
            "completeness": 0.90,
            "proportion": 0.75,
            "visual_quality": 0.80,
            "issues": [
                {{
                    "type": "wrong_position",
                    "target": "motor_01",
                    "description": "...",
                    "severity": "medium"
                }}
            ]
        }}
        ```
        """
```

---

## Data Flow Diagram

```
User ──📷──→ Upload Photos
              │
              ▼
        ┌─────────────┐
        │  Orchestrator│
        │   Agent     │
        └──────┬──────┘
               │
     ┌─────────▼─────────┐
     │  Vision Pipeline   │
     │  ───────────────  │
     │  YOLO: motor(0.95)│
     │  YOLO: pump(0.87) │
     │  GPT4V: "Motor 5HP│
     │  Siemens, pump     │
     │  centrifugal"      │
     └─────────┬─────────┘
               │
               ▼
     ┌─────────────────┐
     │  Asset Matching  │
     │  ──────────────  │
     │  motor_5hp.glb ✅│
     │  pump_centri.glb│
     │  ✅ matched      │
     └─────────┬─────────┘
               │
               ▼
     ┌─────────────────┐
     │  Layout Agent    │
     │  ──────────────  │
     │  pos motor: [x,y]│
     │  pos pump: [x,y] │
     └─────────┬─────────┘
               │
               ▼
     ┌─────────────────┐
     │  Scene Assembler │
     │  ──────────────  │
     │  → motor.glb     │
     │  → pump.glb      │
     │  → lighting      │
     │  → export .glb   │
     └─────────┬─────────┘
               │
               ▼
     ┌─────────────────┐
     │  Preview & Review│
     │  User approves ✅│
     └─────────┬─────────┘
               │
         ┌─────▼─────┐
         │ Digital   │
         │ Twin      │
         │ Ready 🎯  │
         └───────────┘
```

---

## API Contract

### POST /api/agent/3d-generate

```json
{
  "photos": ["motor_front.jpg", "motor_side.jpg", "pump_top.jpg"],
  "floor_plan": "layout.png",
  "factory_id": "fabrik-01",
  "options": {
    "asset_library": ["standard", "custom"],
    "photogrammetry": false,
    "auto_layout": true
  }
}
```

**Response (via WebSocket progress):**
```json
{
  "status": "processing",
  "step": "vision_pipeline",
  "progress": 0.3,
  "detected": [
    {"name": "induction_motor_5hp", "confidence": 0.95, "pose": {...}},
    {"name": "centrifugal_pump", "confidence": 0.87, "pose": {...}}
  ]
}
```

```json
{
  "status": "completed",
  "scene_url": "/scenes/fabrik-01.glb",
  "metadata_url": "/scenes/fabrik-01.json",
  "equipment_list": [...],
  "summary": "Berhasil generate 12 equipment dari 15 foto",
  "unmatched": ["pressure_valve_01"]
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph (Python) |
| Vision | YOLOv8 + Qwen2-VL / LLaVA-1.6 / InternVL2 |
| Photogrammetry | COLMAP + Open3D (opsional) |
| 3D Engine | Three.js / React Three Fiber |
| Scene Export | three-gltf-exporter |
| Asset Matching | CLIP embedding + pgvector |
| Compute | FastAPI + Celery workers |
| Storage | S3 (assets) + PostgreSQL (metadata) |

---

## Hackathon Implementation (Simplified)

Untuk demo, kita bisa simplify dengan **skip photogrammetry** dan fokus ke:

1. **Upload foto** → Vision agent identifikasi equipment
2. **Asset Library** → Match dengan pre-made 3D models
3. **Layout Assistant** → User drag-drop dengan AI suggestion
4. **Auto-positioning** → Berdasarkan bounding box dari foto

```python
# Simplified pipeline pseudo-code
async def generate_3d_scene(photos: list[Image]):
    # 1. Vision
    equipment = await vision_agent.identify(photos)
    # [{name: "conveyor", confidence: 0.92, bbox: [x1,y1,x2,y2]}, ...]
    
    # 2. Match asset
    for eq in equipment:
        eq.asset_3d = await asset_library.match(eq.name)
        # fallback: generate procedural model dari bounding box
    
    # 3. Layout (from photos + floor plan)
    layout = await layout_agent.arrange(equipment, floor_plan)
    
    # 4. Assemble & export
    scene = assemble_3d_scene(equipment, layout)
    export_url = await export_gltf(scene)
    
    return export_url
```

---

## Key Considerations

### What's Realistic for Hackathon
- **Pre-built asset library** — jangan build dari scratch
- **Vision hanya untuk identifikasi**, bukan reconstruction
- **Layout suggestion via LLM** + manual override
- **Procedural fallback** pakai Three.js primitives

### What to Skip
- Pure mesh generation from photos (butuh GPU besar, waktu lama)
- Multi-view photogrammetry (kecuali dataset sudah ada)
- Real-time reconstruction

### Differentiation Factor
→ **AI Agent yang bisa "ngobrol" tentang layout dan equipment**
→ User bisa minta: "tambah conveyor di sini", "geser motor ke kiri"
→ LLM yang handle intent → eksekusi perubahan scene