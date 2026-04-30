# 🎬 Demo Scenario: Hackathon AI Elevate

## 📋 Overview

Demo ini mensimulasikan implementasi **AI Twin Factory** di **Pabrik Baja Nirkarat IMIP**, dengan fokus pada **Zone 1 (Raw Material)** dan **Zone 2 (EAF)**.

**Durasi Demo:** 10-15 menit  
**Target Audience:** Juri hackathon, stakeholders industri  
**Key Message:** "AI-powered digital twin untuk hilirisasi industri Indonesia"

---

## 🎥 Demo Storyline

### Scene 1: Opening (1 menit)
**Visual:** Video pengenalan proyek hilirisasi Indonesia

**Narrator:**
> "Presiden Prabowo Subianto baru saja meresmikan 13 proyek hilirisasi senilai Rp 116 triliun. Salah satunya adalah Pabrik Baja Nirkarat di IMIP dengan kapasitas 1,2 juta ton per tahun. Tapi ada tantangan besar: bagaimana memastikan pabrik ini beroperasi 24/7 dengan efisiensi tinggi?"

**Transition:** Logo AI Twin Factory

---

### Scene 2: Problem Statement (2 menit)
**Visual:** Split screen - problem vs solution

**Left Side (Problem):**
- Pabrik baja: ratusan equipment, high temperature, critical processes
- Equipment failure = downtime Rp 5 juta/jam
- Maintenance manual & reactive
- Setup digital twin: 3 minggu + Rp 500 juta

**Right Side (Solution):**
- AI Twin Factory: 3 komponen utama
- 1. AI-Driven 3D Modeling
- 2. Smart Monitoring  
- 3. AI Decision Agent

---

### Scene 3: 3D Reconstruction (3 menit)

**Demo Steps:**

1. **Upload Photos** (30 detik)
   ```
   User: Upload 10 foto Zone 1 (Raw Material Handling)
   - Foto conveyor dari angle depan, samping, atas
   - Foto EAF dari jarak aman
   - Floor plan pabrik
   ```
   
2. **AI Processing** (real-time visualization)
   ```
   System Status:
   → Extracting equipment... [██████░░░░] 60%
   → Identifying: Conveyor C-01, C-02, C-03 ✓
   → Identifying: EAF-01, EAF-02 ✓
   → Estimating poses... [████████░░] 80%
   → Matching assets... [██████████] 100%
   → Assembling 3D scene...
   ```

3. **3D Scene Render** (1 menit)
   - Rotate, zoom, pan
   - Click equipment → show metadata
   - Highlight: "Conveyor C-03: 120m, 500 ton/hour capacity"

4. **Self-Evaluation Result**
   ```
   Evaluation Score:
   • Equipment Completeness: 0.92 ✓
   • Position Accuracy: 0.88 ✓
   • Scale/Proportion: 0.90 ✓
   • Visual Quality: 0.85 ✓
   ─────────────────────────
   Total: 0.89 (PASSED)
   ```

---

### Scene 4: Smart Monitoring (3 menit)

**Visual:** Real-time dashboard dengan 3D scene

**Demo Steps:**

1. **Sensor Data Flow** (1 menit)
   ```
   Live Sensor Feed:
   
   Conveyor C-03:
   ├─ Vibration (RMS): 4.2 mm/s [████████░░] NORMAL
   ├─ Motor Temp: 68°C [████████░░] NORMAL
   ├─ Current (R): 32.5A [████████░░] NORMAL
   └─ Belt Tracking: ±1.2mm [████████░░] NORMAL
   
   EAF-01:
   ├─ Furnace Temp: 1650°C [████████░░] NORMAL
   ├─ Electrode Current: 45kA [████████░░] NORMAL
   └─ Cooling Pressure: 4.8 bar [████████░░] NORMAL
   ```

2. **Anomaly Injection** (operator trigger)
   ```
   ⚠️ ANOMALI TERDETEKSI!
   
   Equipment: Conveyor C-03
   Sensor: Vibration Drive End
   Value: 12.5 mm/s (Normal: <5 mm/s)
   Status: 🔴 CRITICAL
   
   [VIEW IN 3D] [ACKNOWLEDGE] [ESCALATE]
   ```

3. **3D Visualization Alert**
   - Conveyor C-03 highlighted red (pulsing)
   - Camera auto-zoom ke equipment
   - Show alert panel di sidebar

---

### Scene 5: AI Decision Agent (3 menit)

**Visual:** Chat interface dengan AI agent

**Demo Steps:**

1. **AI Analysis** (1 menit)
   ```
   🤖 AI MAINTENANCE EXPERT
   
   Analyzing anomaly on Conveyor C-03...
   
   ✓ Vibration spectrum analysis complete
   ✓ Historical data comparison complete
   ✓ Similar incidents retrieved (3 cases)
   ✓ Equipment manual consulted
   
   ─────────────────────────────────────
   
   📊 DIAGNOSIS:
   
   Root Cause: Bearing outer race defect
   Confidence: 94%
   
   Evidence:
   • BPFO frequency spike detected (156.2 Hz)
   • Temperature rise: 68°C → 78°C (3 days)
   • Current increase: 32A → 36A (loading)
   
   Similar Case: CONV-C05 (Feb 2026)
   → Bearing replaced, no secondary damage
   
   ─────────────────────────────────────
   
   🚨 SEVERITY: HIGH
   Time to Failure: 48-72 hours
   
   💰 IMPACT ANALYSIS:
   • If not handled: Breakdown in 2-3 days
   • Production loss: 180 ton stainless steel
   • Financial impact: Rp 15 miliar
   
   ─────────────────────────────────────
   
   📋 RECOMMENDED ACTIONS:
   
   1. 🔴 URGENT: Schedule bearing replacement
      Priority: HIGH
      Timeline: Within 24 hours
      Reason: Prevent catastrophic failure
      
   2. 🟡 Prepare spare parts:
      • Bearing SKF 22320 CC/W33 (2 pcs)
      • Grease LGHP 2 (5 kg)
      • Estimated cost: Rp 45 juta
      
   3. 🟡 Assign technician:
      • Pak Suyanto (Bearing Specialist)
      • Shift: Day shift (08:00-16:00)
      • Duration: 4 hours
      
   4. 🟢 Coordinate production:
      • Buffer material untuk EAF
      • EAF can operate 6 hours without C-03
      • Optimal window: Tomorrow 14:00-18:00
   ```

2. **User Interaction** (1 menit)
   ```
   User: "What if we delay to next week?"
   
   AI: "⚠️ NOT RECOMMENDED
   
   Risk Analysis:
   • 65% probability bearing will fail completely
   • Secondary damage: Drive motor (Rp 800 juta)
   • Emergency shutdown: 12-24 hours downtime
   • Total potential loss: Rp 25-40 miliar
   
   Recommendation: Proceed with 24-hour schedule"
   
   ─────────────────────────────────────
   
   User: "Create work order"
   
   AI: "✅ Work Order Created: #WO-2026-0442
   
   • Equipment: CONV-C03
   • Task: Bearing replacement
   • Scheduled: Tomorrow 14:00-18:00
   • Assigned: Pak Suyanto
   • Spares: Reserved from warehouse
   • Notifications sent to:
    - Maintenance Supervisor
    - Plant Manager
    - Production Planner
   
   [VIEW IN CMMS] [PRINT WO] [MODIFY]"
   ```

3. **Work Order Visualization** (1 menit)
   - Show 3D scene dengan maintenance marker
   - Highlight equipment yang akan di-maintain
   - Show spare parts location di warehouse

---

### Scene 6: Impact & Closing (2 menit)

**Visual:** Before/After comparison

**Left Side (Without AI Twin Factory):**
- ❌ Reactive maintenance
- ❌ 8-12% unplanned downtime
- ❌ Equipment failure = panic mode
- ❌ Manual inspection tiap hari
- ❌ Setup digital twin: 3 minggu + Rp 500 juta

**Right Side (With AI Twin Factory):**
- ✅ Predictive maintenance
- ✅ <2% unplanned downtime
- ✅ Early warning 48-72 jam sebelum failure
- ✅ AI assistant 24/7
- ✅ Setup digital twin: 2 hari + Rp 50 juta

**KPI Dashboard:**
```
┌─────────────────────────────────────────────────────────┐
│  IMPACT METRICS - PABRIK BAJA NIRKARAT IMIP            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🎯 OPERATIONAL                                          │
│  • Unplanned Downtime:     10% → 1.5%   ↓ 85%           │
│  • Equipment Availability: 88% → 96%    ↑ 8%            │
│  • OEE:                    65% → 85%    ↑ 30%           │
│  • MTTR:                   5 jam → 1.5 jam  ↓ 70%       │
│                                                          │
│  💰 FINANCIAL (Annual)                                   │
│  • Avoided Downtime:       Rp 35 miliar                 │
│  • Maintenance Savings:    Rp 15 miliar                 │
│  • Inventory Optimization: Rp 8 miliar                  │
│  • Energy Efficiency:      Rp 12 miliar                 │
│  ─────────────────────────────────────────               │
│  • TOTAL BENEFIT:          Rp 75 miliar/tahun           │
│  • ROI:                    1,500% (Payback: 1 month)    │
│                                                          │
│  🏭 STRATEGIC                                            │
│  • Mendukung hilirisasi 1,2 juta ton stainless steel   │
│  • Menciptakan lapangan kerja berkualitas              │
│  • Meningkatkan daya saing industri nasional           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Closing Statement:**
> "AI Twin Factory: Membuat pabrik hilirisasi Indonesia beroperasi dengan efisiensi dan keandalan kelas dunia. Dari IMIP, menuju 600.000 lapangan kerja baru, menuju Indonesia Emas 2045."

---

## 🎭 Demo Roles

| Role | Person | Script |
|------|--------|--------|
| **Narrator** | Presenter 1 | Opening, closing, transitions |
| **Operator** | Presenter 2 | Upload photos, trigger anomalies, interact with AI |
| **AI Voice** | Text-to-speech / Voiceover | AI agent responses |

---

## 🛠️ Technical Setup

### Hardware Requirements
- **Laptop:** GPU capable (RTX 3060+ recommended)
- **Display:** External monitor/TV for demo
- **Internet:** Stable connection (untuk API calls)
- **Backup:** Video recording sebagai fallback

### Software Checklist
- [ ] MapAnything model downloaded
- [ ] Qwen2.5 via Ollama running
- [ ] Frontend app running (localhost:3000)
- [ ] Backend API running (localhost:8000)
- [ ] Demo dataset (photos) prepared
- [ ] Mock sensor data generator running

### Demo Data
```
/demo-data/
├── zone1-photos/
│   ├── conveyor_c01_front.jpg
│   ├── conveyor_c01_side.jpg
│   ├── conveyor_c01_top.jpg
│   ├── conveyor_c02_front.jpg
│   ├── ... (10-15 photos)
│   └── floor_plan.png
├── zone2-photos/
│   ├── eaf_01_distance.jpg
│   ├── eaf_01_closeup.jpg
│   └── ...
└── mock-sensor-data/
    └── conveyor_c03_anomaly.csv
```

---

## ⚠️ Risk Mitigation

| Risk | Mitigation |
|------|------------|
| 3D reconstruction slow | Use pre-generated scene sebagai backup |
| LLM API down | Use local Ollama (Qwen2.5) |
| Sensor simulation error | Hardcode demo scenario |
| Demo crash | Video recording sebagai fallback |
| Time over | Skip scene 1, fokus ke 3D + AI demo |

---

## 📝 Q&A Preparation

**Q: Kenapa pilih Pabrik Baja Nirkarat?**  
A: Proyek hilirisasi strategis nasional, equipment kompleks, high impact jika berhasil.

**Q: Bagaimana dengan data privacy?**  
A: Semua AI model bisa di-deploy on-premise (Ollama), data tidak keluar dari pabrik.

**Q: Skalabilitas ke pabrik lain?**  
A: Framework modular, bisa di-apply ke smelter, kilang, atau pabrik manufaktur lainnya.

**Q: Training data requirement?**  
A: Unsupervised learning untuk anomaly detection (tidak perlu label data abnormal). 3D reconstruction pakai foundation model (MapAnything) yang pre-trained.

**Q: Integration dengan existing SCADA?**  
A: MQTT/Modbus bridge untuk sensor, REST API untuk control systems.

---

## 🎨 Visual Assets

### Slides Needed
1. Cover: "AI Twin Factory for Stainless Steel Plant"
2. Indonesia Hilirisasi Context
3. Problem Statement
4. Solution Architecture (5-layer)
5. 3D Reconstruction Demo (screenshots)
6. Smart Monitoring Dashboard
7. AI Decision Agent (chat interface)
8. Impact Metrics
9. Roadmap
10. Team & Closing

### Video Clips
- [ ] Presiden Prabowo groundbreaking ceremony (10 detik)
- [ ] Pabrik baja operations (B-roll)
- [ ] 3D visualization rotation ( looping)

---

## ✅ Pre-Demo Checklist

**1 Week Before:**
- [ ] Finalize code & test end-to-end
- [ ] Record backup video
- [ ] Prepare demo dataset
- [ ] Rehearse script

**1 Day Before:**
- [ ] Test hardware setup
- [ ] Verify all services running
- [ ] Download offline models
- [ ] Prepare Q&A answers

**Demo Day:**
- [ ] Arrive early, setup equipment
- [ ] Run smoke test (3D + AI)
- [ ] Have backup video ready
- [ ] Relax & present with confidence! 🚀

---

**Good luck team! 🇮🇩🔥**
