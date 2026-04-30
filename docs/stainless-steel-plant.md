# 🏭 Reference Architecture: Pabrik Baja Nirkarat (Stainless Steel Plant)

## 📋 Overview

Dokumen ini mendeskripsikan implementasi **AI Twin Factory** untuk **Fasilitas Manufaktur Baja Nirkarat** di Indonesia Morowali Industrial Park (IMIP), Sulawesi Tengah - sebagai bagian dari Proyek Hilirisasi Fase 2 yang diresmikan oleh Presiden Prabowo Subianto.

---

## 🎯 Project Context

| Parameter | Detail |
|-----------|--------|
| **Proyek** | Fasilitas Manufaktur Baja Nirkarat dari Nikel |
| **Lokasi** | Indonesia Morowali Industrial Park (IMIP), Sulawesi Tengah |
| **Kapasitas** | 1,2 juta ton stainless steel slab per tahun |
| **Investor** | PT Krakatau Steel (Persero) Tbk + Tsingshan Group |
| **Proses** | Peleburan + Pemurnian modern (smelting & refining) |
| **Hilirisasi Fase** | Fase 2 (13 proyek, Rp 116 triliun total) |

---

## 🏗️ Plant Layout & Zones

```
┌─────────────────────────────────────────────────────────────────────┐
│              PABRIK BAJA NIRKARAT - IMIP LAYOUT                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ZONE 1: RAW MATERIAL HANDLING                                 │  │
│  │  • Nickel ore storage & screening                          │  │
│  │  • Conveyor C-01 to C-05 (transport to EAF)                │  │
│  │  • Crusher & grinder systems                               │  │
│  │  • Bucket elevators                                        │  │
│  │  [Sensors: Vibration, Current, Temperature]                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ZONE 2: ELECTRIC ARC FURNACE (EAF)                            │  │
│  │  • EAF Furnace (3 units, 90 MW each)                       │  │
│  │  • Electrode positioner systems                            │  │
│  │  • Charging system                                         │  │
│  │  • Fume extraction & gas cleaning                          │  │
│  │  • Cooling pumps & heat exchangers                         │  │
│  │  [Sensors: Temp (>1600°C), Pressure, Current, Vibration]   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ZONE 3: ARGON OXYGEN DECARBURIZATION (AOD)                    │  │
│  │  • AOD Converter (refining process)                        │  │
│  │  • Lance systems (O2 + Ar injection)                       │  │
│  │  • Stirring gas systems                                    │  │
│  │  [Sensors: Gas flow, Pressure, Temperature]                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ZONE 4: CONTINUOUS CASTING                                    │  │
│  │  • Ladle turret (rotation mechanism)                       │  │
│  │  • Tundish (molten steel distribution)                     │  │
│  │  • Mold assemblies (copper molds)                          │  │
│  │  • Secondary cooling (water sprays)                        │  │
│  │  • Withdrawal rolls & drive systems                        │  │
│  │  • Cutting & torch systems                                 │  │
│  │  [Sensors: Temp, Flow, Position, Thickness]                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ZONE 5: HOT ROLLING MILL                                      │  │
│  │  • Reheating furnace                                       │  │
│  │  • Roughing mill (3-stand)                                 │  │
│  │  • Intermediate/finishing mill (7-stand)                   │  │
│  │  • Cooling bed                                             │  │
│  │  • Coiling station                                         │  │
│  │  [Sensors: Vibration, Thickness, Temp, Force]              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ ZONE 6: FINISHING & STORAGE                                   │  │
│  │  • Annealing & pickling lines                              │  │
│  │  • Slitting & cutting lines                                │  │
│  │  • Quality inspection                                      │  │
│  │  • Storage yard                                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📡 Equipment & Sensor Mapping

### Critical Equipment List

| Equipment ID | Type | Zone | Criticality | Sensor Types |
|--------------|------|------|-------------|--------------|
| **EAF-01/02/03** | Electric Arc Furnace | Zone 2 | CRITICAL | Temp, Current, Vibration, Pressure |
| **CONV-C01-C10** | Belt Conveyor | Zone 1 | HIGH | Vibration, Current, Belt tracking |
| **PUMP-P01-P20** | Cooling Pump | Zone 2,4 | HIGH | Flow, Pressure, Temp, Vibration |
| **MOTOR-M50-M150** | AC Motors (various) | All | MEDIUM | Current, Vibration, Temp |
| **ROLL-R01-R30** | Rolling Mill Rolls | Zone 5 | HIGH | Force, Vibration, Thickness |
| **LADLE-L01-L08** | Ladle Turret | Zone 4 | CRITICAL | Position, Load, Rotation |
| **FAN-F01-F15** | Fume Extraction | Zone 2 | MEDIUM | Flow, Vibration, Current |

### Sensor Specifications

```yaml
# Example: EAF Conveyor System
conveyor_c03:
  equipment_type: "Belt Conveyor"
  location: "Zone 1 → Zone 2"
  length: "120 meters"
  capacity: "500 ton/hour"
  
  sensors:
    vibration:
      type: "IEPE Accelerometer"
      position: ["Drive end", "Tail end", "Intermediate"]
      range: "0-50 mm/s"
      sampling: "10 kHz"
      features: ["RMS", "Peak", "FFT Spectrum"]
      
    temperature:
      type: "IR Pyrometer + RTD"
      position: ["Motor bearing", "Gearbox", "Belt surface"]
      range: "0-150°C"
      sampling: "1 Hz"
      
    current:
      type: "Hall Effect CT"
      phases: ["R", "S", "T"]
      range: "0-200A"
      sampling: "1 kHz"
      features: ["RMS", "Harmonics"]
      
    belt_tracking:
      type: "Ultrasonic sensor"
      position: ["Head pulley", "Tail pulley"]
      accuracy: "±2 mm"
```

---

## 🔍 Anomaly Detection Scenarios

### Scenario 1: Conveyor Bearing Failure

**Pattern Detected:**
- Vibration spike di frekuensi BPFO (Ball Pass Frequency Outer)
- Temperature gradual rise 3°C/day
- Current draw increase 12%

**ML Model:** Isolation Forest + Statistical Threshold

**Decision Agent Action:**
```json
{
  "equipment": "CONV-C03",
  "anomaly_type": "bearing_wear",
  "severity": "HIGH",
  "time_to_failure": "48-72 hours",
  "recommended_action": "Schedule replacement during next EAF maintenance window",
  "spare_parts": ["SKF 22320 CC/W33", "Grease LGHP 2"],
  "estimated_cost_avoided": "Rp 8.5 miliar"
}
```

### Scenario 2: EAF Electrode Breakage Risk

**Pattern Detected:**
- Current fluctuations anomalous
- Electrode consumption rate 15% above normal
- Vibration unusual saat arc formation

**ML Model:** LSTM Autoencoder (temporal pattern)

**Decision Agent Action:**
- CRITICAL alert ke furnace operator
- Suggest reduce power input
- Prepare electrode joining equipment standby

### Scenario 3: Cooling Pump Cavitation

**Pattern Detected:**
- Pressure drop > 0.5 bar dalam 10 detik
- Vibration frekuensi tinggi (>5 kHz)
- Flow rate decrease 20%

**ML Model:** Statistical Filter (instant)

**Decision Agent Action:**
- Auto-switch ke backup pump
- Isolate affected pump
- Schedule inspection

---

## 🎨 3D Reconstruction Workflow

### Input Data
- **Photos:** 50-100 foto dari setiap zone
- **Layout:** CAD drawing / site plan (PDF/DWG)
- **Reference:** Known dimensions (column spacing, equipment footprint)

### Processing Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: MapAnything 3D Reconstruction                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Input: Zone photos (multi-angle)                             │
│        ↓                                                     │
│ MapAnything VLM:                                             │
│   • Detect equipment boundaries                              │
│   • Estimate poses (position + rotation)                     │
│   • Generate point cloud                                     │
│        ↓                                                     │
│ Output: 3D scene dengan equipment poses                      │
│         Format: COLMAP / GLB                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 2: Asset Matching & Enhancement                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ For each detected equipment:                                 │
│   • CLIP embedding dari visual features                      │
│   • Search asset library (conveyor, motor, pump, etc.)       │
│   • If match > 0.85: Replace dengan high-quality 3D model   │
│   • Else: Keep MapAnything mesh                              │
│                                                              │
│ Asset Library (Industrial):                                  │
│   /assets/                                                   │
│     ├── conveyors/                                           │
│     │   ├── belt_conveyor_120m.glb                         │
│     │   └── bucket_elevator_50m.glb                        │
│     ├── furnaces/                                            │
│     │   └── electric_arc_furnace_90mw.glb                  │
│     ├── pumps/                                               │
│     │   ├── centrifugal_pump_500hp.glb                     │
│     │   └── cooling_pump_200hp.glb                         │
│     ├── motors/                                              │
│     │   ├── ac_motor_100hp.glb                             │
│     │   └── ac_motor_500hp.glb                             │
│     └── mills/                                               │
│         ├── roughing_mill_3stand.glb                       │
│         └── finishing_mill_7stand.glb                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 3: Sensor Integration & Metadata                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ For each 3D equipment model:                                 │
│   • Attach sensor mapping (sensor_id → equipment_id)         │
│   • Add maintenance metadata (install date, last service)    │
│   • Link equipment manual (PDF)                              │
│   • Set alert thresholds (per sensor)                        │
│                                                              │
│ Metadata JSON:                                               │
│ {                                                            │
│   "equipment_id": "CONV-C03",                                │
│   "zone": "Zone 1",                                          │
│   "type": "belt_conveyor",                                   │
│   "position": [x, y, z],                                     │
│   "sensors": {                                               │
│     "vibration": "sensor_vib_c03_drive",                     │
│     "temperature": "sensor_temp_c03_motor",                  │
│     "current": "sensor_curr_c03_r",                          │
│     "current": "sensor_curr_c03_s",                          │
│     "current": "sensor_curr_c03_t"                           │
│   },                                                         │
│   "thresholds": {                                            │
│     "vibration_rms": { "warning": 4.5, "critical": 7.0 },   │
│     "temp_motor": { "warning": 80, "critical": 95 }         │
│   },                                                         │
│   "maintenance": {                                           │
│     "last_service": "2026-03-15",                            │
│     "next_scheduled": "2026-06-15",                          │
│     "critical_components": ["bearing_drive", "belt_joint"]   │
│   }                                                          │
│ }                                                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 4: Self-Evaluation                                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Render 4 views dari 3D scene:                                │
│   • Bird eye view (top-down)                                 │
│   • Operator eye level (1.7m height)                         │
│   • Equipment close-up                                       │
│   • Full plant overview                                      │
│                                                              │
│ VLM (Qwen2-VL) evaluate:                                     │
│   "Does this 3D scene match the reference photos?"           │
│                                                              │
│ Scoring:                                                     │
│   • Equipment completeness: 0-1.0                            │
│   • Position accuracy: 0-1.0                                 │
│   • Scale/proportion: 0-1.0                                  │
│   • Visual quality: 0-1.0                                    │
│                                                              │
│ If total < 0.8: Trigger re-generation dengan adjusted params│
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Success Metrics

### Operational KPIs

| Metric | Baseline (Manual) | With AI Twin Factory | Improvement |
|--------|-------------------|----------------------|-------------|
| **Unplanned Downtime** | 8-12% | < 2% | ↓ 80% |
| **Mean Time to Repair (MTTR)** | 4-6 hours | 1-2 hours | ↓ 70% |
| **Equipment Availability** | 88% | 96% | ↑ 8% |
| **OEE (Overall Equipment Effectiveness)** | 65% | 85% | ↑ 30% |
| **Maintenance Cost** | 100% | 60% | ↓ 40% |
| **Safety Incidents** | 5-10/year | < 2/year | ↓ 75% |

### Digital Twin KPIs

| Metric | Target |
|--------|--------|
| **3D Setup Time** | 2 days vs 3 weeks |
| **3D Accuracy** | > 85% (vs site survey) |
| **Alert Response Time** | < 5 seconds (critical) |
| **False Positive Rate** | < 5% |
| **User Adoption** | > 80% operators use weekly |

---

## 💰 Business Impact Estimation

### Cost Avoidance (Annual)

| Category | Calculation | Value |
|----------|-------------|-------|
| **Avoided Downtime** | 10% → 2% downtime reduction × Rp 5M/jam × 8760 jam | Rp 35 miliar |
| **Maintenance Optimization** | Predictive vs reactive (30% cost reduction) | Rp 15 miliar |
| **Spare Parts Inventory** | Right-sizing inventory (20% reduction) | Rp 8 miliar |
| **Safety Incidents** | Fewer accidents, insurance savings | Rp 5 miliar |
| **Energy Efficiency** | Optimal equipment operation (5% saving) | Rp 12 miliar |
| **TOTAL** | | **Rp 75 miliar/tahun** |

### ROI Analysis

- **Initial Investment:** Rp 5 miliar (platform development + deployment)
- **Annual Benefit:** Rp 75 miliar
- **Payback Period:** 1 month
- **3-Year NPV:** Rp 215 miliar

---

## 🚀 Implementation Roadmap

### Phase 1: Pilot (Month 1-3)
- **Zone:** Zone 1 (Raw Material) + Zone 2 (EAF)
- **Equipment:** 10 critical conveyors + 3 EAF units
- **Sensors:** 50 vibration + temp sensors
- **Goal:** Prove anomaly detection accuracy

### Phase 2: Expansion (Month 4-8)
- **Zone:** Add Zone 4 (Continuous Casting)
- **Equipment:** +30 pumps, ladles, casting machines
- **Sensors:** Total 200 sensors
- **Goal:** Full 3D visualization + predictive maintenance

### Phase 3: Full Plant (Month 9-12)
- **Zone:** All 6 zones
- **Equipment:** 150+ equipment units
- **Sensors:** 500+ sensors
- **Goal:** Plant-wide digital twin + AI optimization

---

## 📚 Related Documents

- [System Architecture](../README.md#-arsitektur-sistem-5-layer)
- [Layer 3 AI/ML Details](./layer3-detailed.md)
- [MapAnything 3D Reconstruction Guide](./mapanything-integration.md)
- [API Documentation](./api-reference.md) (coming soon)

---

## 🙏 Acknowledgment

Proyek ini dikembangkan untuk mendukung **program hilirisasi nasional** dan **visi Indonesia Emas 2045**. Terima kasih kepada:
- PT Krakatau Steel & Tsingshan Group
- Kementerian Investasi dan Hilirisasi (BKPM)
- Danantara ( sovereign wealth fund Indonesia)
- Seluruh stakeholder proyek hilirisasi Indonesia
