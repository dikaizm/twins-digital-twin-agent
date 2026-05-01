import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np


class SensorDataset(Dataset):
    def __init__(self, sequences: np.ndarray, labels: np.ndarray = None):
        self.sequences = torch.FloatTensor(sequences)
        self.labels = torch.FloatTensor(labels) if labels is not None else None

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int):
        if self.labels is not None:
            return self.sequences[idx], self.labels[idx]
        return self.sequences[idx]


def create_dataloaders(
    train_data: np.ndarray,
    val_data: np.ndarray,
    test_data: np.ndarray,
    batch_size: int = 32,
    labels: dict = None
) -> dict:
    loaders = {}

    train_dataset = SensorDataset(train_data, labels.get("train") if labels else None)
    loaders["train"] = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    val_dataset = SensorDataset(val_data, labels.get("val") if labels else None)
    loaders["val"] = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    test_dataset = SensorDataset(test_data, labels.get("test") if labels else None)
    loaders["test"] = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return loaders
