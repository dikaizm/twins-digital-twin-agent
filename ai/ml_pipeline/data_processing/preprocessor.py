import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.preprocessing import StandardScaler, RobustScaler


class DataPreprocessor:
    def __init__(self, scaler_type: str = "robust"):
        self.scaler_type = scaler_type
        self.scaler = RobustScaler() if scaler_type == "robust" else StandardScaler()
        self.fitted = False

    def fit(self, data: np.ndarray) -> "DataPreprocessor":
        self.scaler.fit(data)
        self.fitted = True
        return self

    def transform(self, data: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Preprocessor must be fitted before transform")
        return self.scaler.transform(data)

    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        self.fit(data)
        return self.transform(data)

    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        return self.scaler.inverse_transform(data)


def create_sequences(data: np.ndarray, seq_len: int = 60, step: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(0, len(data) - seq_len, step):
        X.append(data[i:i + seq_len])
        y.append(data[i + seq_len])
    return np.array(X), np.array(y)


def compute_statistical_features(data: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame()

    for col in data.select_dtypes(include=[np.number]).columns:
        values = data[col].values

        features[f"{col}_mean"] = pd.Series(values).rolling(10, min_periods=1).mean().values
        features[f"{col}_std"] = pd.Series(values).rolling(10, min_periods=1).std().fillna(0).values
        features[f"{col}_min"] = pd.Series(values).rolling(10, min_periods=1).min().values
        features[f"{col}_max"] = pd.Series(values).rolling(10, min_periods=1).max().values
        features[f"{col}_skew"] = pd.Series(values).rolling(10, min_periods=1).skew().fillna(0).values
        features[f"{col}_kurtosis"] = pd.Series(values).rolling(10, min_periods=1).kurt().fillna(0).values

    return features


def detect_outliers_zscore(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    z_scores = np.abs((data - mean) / (std + 1e-8))
    return np.any(z_scores > threshold, axis=1)


def detect_outliers_iqr(data: np.ndarray, factor: float = 1.5) -> np.ndarray:
    Q1 = np.percentile(data, 25, axis=0)
    Q3 = np.percentile(data, 75, axis=0)
    IQR = Q3 - Q1
    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR
    return np.any((data < lower) | (data > upper), axis=1)


def validate_sequence_lengths(data: pd.DataFrame, seq_len: int, overlap: float = 0.5) -> bool:
    min_samples = seq_len
    return len(data) >= min_samples
