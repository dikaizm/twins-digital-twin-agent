# ML Training & Evaluation Pipeline

## Overview

Pipeline untuk training dan evaluasi anomaly detection model dengan 3 approach:
1. **Isolation Forest** - Multi-variate anomaly detection
2. **LSTM Autoencoder** - Temporal pattern recognition
3. **Ensemble** - Combined scoring

## Pipeline Structure

```
data/
├── raw/                    # Raw sensor data
├── processed/              # Preprocessed features
├── train/                  # Training set
├── val/                    # Validation set
└── test/                   # Test set

models/
├── isolation_forest/       # IF model artifacts
├── lstm_autoencoder/       # LSTM model artifacts
└── ensemble/               # Combined model

outputs/
├── metrics/                 # Evaluation metrics
├── plots/                   # Visualization plots
└── reports/                # Training reports
```

## Quick Start

```bash
cd ai

# Install dependencies
pip install -r ml_pipeline/requirements-ml.txt

# Generate mock data
python -m ml_pipeline.data_processing.mock_data

# Run full pipeline (train + eval)
python -m ml_pipeline.pipeline run --config ml_pipeline/configs/train_config.yaml
```

## Pipeline Structure

```
ml_pipeline/
├── configs/          # Training configuration
├── data_processing/  # Data preprocessing & mock data generation
├── models/           # Model architectures (LSTM Autoencoder, Isolation Forest)
├── training/          # Training loop with early stopping
├── evaluation/        # Metrics and evaluation
└── pipeline.py       # Main orchestration
```

## Models

1. **Isolation Forest** - Multi-variate anomaly detection (sklearn)
2. **LSTM Autoencoder** - Temporal pattern recognition (PyTorch)
3. **Ensemble** - Combined scoring with weighted average
