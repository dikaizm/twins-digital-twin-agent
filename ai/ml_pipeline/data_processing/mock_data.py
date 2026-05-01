import yaml
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple
from sklearn.model_selection import train_test_split


class MockDataGenerator:
    def __init__(
        self,
        n_samples: int = 10000,
        n_features: int = 12,
        anomaly_ratio: float = 0.05,
        seq_len: int = 60
    ):
        self.n_samples = n_samples
        self.n_features = n_features
        self.anomaly_ratio = anomaly_ratio
        self.seq_len = seq_len

    def generate_normal_data(self, n: int) -> np.ndarray:
        t = np.linspace(0, 4 * np.pi, n)
        data = np.zeros((n, self.n_features))

        data[:, 0] = 100 + 10 * np.sin(t * 0.1) + np.random.normal(0, 2, n)
        data[:, 1] = 150 + 15 * np.cos(t * 0.15) + np.random.normal(0, 3, n)
        data[:, 2] = 200 + 12 * np.sin(t * 0.2 + 1) + np.random.normal(0, 2.5, n)
        data[:, 3] = 50 * np.exp(-t * 0.01) + np.random.normal(0, 5, n)
        data[:, 4] = 80 + 20 * np.sin(t * 0.05) + np.random.normal(0, 3, n)

        for i in range(5, self.n_features):
            base = 100 + i * 10
            data[:, i] = base + 5 * np.sin(t * 0.1 * i) + np.random.normal(0, 2, n)

        return data

    def inject_anomalies(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        n_anomalies = int(self.n_samples * self.anomaly_ratio)
        labels = np.zeros(len(data))
        data = data.copy()

        n_point_anomalies = int(n_anomalies * 0.7)
        idx = np.random.choice(len(data), n_point_anomalies, replace=False)
        data[idx] += np.random.normal(0, 15, (n_point_anomalies, self.n_features))
        labels[idx] = 1

        n_contextual_anomalies = int(n_anomalies * 0.2)
        idx = np.random.choice(len(data) - self.seq_len, n_contextual_anomalies, replace=False)
        for i in idx:
            start = i
            end = i + self.seq_len
            data[start:end] += np.random.normal(5, 3, (self.seq_len, self.n_features))
            labels[start:end] = 1

        n_collective_anomalies = n_anomalies - n_point_anomalies - n_contextual_anomalies
        idx = np.random.choice(len(data) - 2 * self.seq_len, n_collective_anomalies, replace=False)
        for i in idx:
            start = i
            end = i + 2 * self.seq_len
            trend = np.linspace(0, 20, 2 * self.seq_len)
            data[start:end] += trend[:, np.newaxis]
            labels[start:end] = 1

        return data, labels

    def generate(self) -> Tuple[np.ndarray, np.ndarray]:
        data = self.generate_normal_data(self.n_samples)
        data, labels = self.inject_anomalies(data)
        return data, labels

    def generate_dataset(self, output_dir: str = "data/raw"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        data, labels = self.generate()

        indices = np.arange(len(data))
        train_idx, temp_idx = train_test_split(indices, test_size=0.3, random_state=42)
        val_idx, test_idx = train_test_split(temp_idx, test_size=0.5, random_state=42)

        train_data, train_labels = data[train_idx], labels[train_idx]
        val_data, val_labels = data[val_idx], labels[val_idx]
        test_data, test_labels = data[test_idx], labels[test_idx]

        np.save(f"{output_dir}/train_data.npy", train_data)
        np.save(f"{output_dir}/train_labels.npy", train_labels)
        np.save(f"{output_dir}/val_data.npy", val_data)
        np.save(f"{output_dir}/val_labels.npy", val_labels)
        np.save(f"{output_dir}/test_data.npy", test_data)
        np.save(f"{output_dir}/test_labels.npy", test_labels)

        print(f"Generated dataset saved to {output_dir}/")
        print(f"  Train: {len(train_data)} samples ({np.sum(train_labels):.0f} anomalies)")
        print(f"  Val: {len(val_data)} samples ({np.sum(val_labels):.0f} anomalies)")
        print(f"  Test: {len(test_data)} samples ({np.sum(test_labels):.0f} anomalies)")


if __name__ == "__main__":
    generator = MockDataGenerator(n_samples=10000, n_features=12, anomaly_ratio=0.05)
    generator.generate_dataset()
