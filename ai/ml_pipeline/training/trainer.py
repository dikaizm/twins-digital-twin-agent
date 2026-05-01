import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
import numpy as np
from tqdm import tqdm
from typing import Optional, Tuple
from pathlib import Path


class Trainer:
    def __init__(
        self,
        model: nn.Module,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.model = model.to(device)
        self.device = device
        self.optimizer: Optional[Adam] = None
        self.scheduler: Optional[ReduceLROnPlateau] = None
        self.train_losses: list = []
        self.val_losses: list = []

    def compile(self, lr: float = 0.001):
        self.optimizer = Adam(self.model.parameters(), lr=lr)
        self.scheduler = ReduceLROnPlateau(self.optimizer, mode="min", factor=0.5, patience=5)

    def train_step(self, batch: torch.Tensor) -> float:
        self.model.train()
        self.optimizer.zero_grad()

        recon, _ = self.model(batch.to(self.device))
        loss = nn.MSELoss()(recon, batch.to(self.device))
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def validate(self, val_loader: DataLoader) -> float:
        self.model.eval()
        total_loss = 0.0

        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(self.device)
                recon, _ = self.model(batch)
                loss = nn.MSELoss()(recon, batch)
                total_loss += loss.item()

        return total_loss / len(val_loader)

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 50,
        early_stopping_patience: int = 10,
        checkpoint_dir: Optional[str] = None
    ) -> dict:
        if self.optimizer is None:
            self.compile()

        best_val_loss = float("inf")
        patience_counter = 0

        for epoch in range(epochs):
            train_loss = 0.0
            for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
                if isinstance(batch, tuple):
                    batch = batch[0]
                train_loss += self.train_step(batch)

            train_loss /= len(train_loader)
            val_loss = self.validate(val_loader)

            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)

            self.scheduler.step(val_loss)

            print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}")

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                if checkpoint_dir:
                    self.save_checkpoint(checkpoint_dir, "best_model.pt")
            else:
                patience_counter += 1
                if patience_counter >= early_stopping_patience:
                    print(f"Early stopping at epoch {epoch+1}")
                    break

        return {"train_losses": self.train_losses, "val_losses": self.val_losses}

    def save_checkpoint(self, path: str, filename: str = "checkpoint.pt"):
        Path(path).mkdir(parents=True, exist_ok=True)
        torch.save({
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
            "train_losses": self.train_losses,
            "val_losses": self.val_losses
        }, f"{path}/{filename}")

    def load_checkpoint(self, path: str, filename: str = "best_model.pt"):
        checkpoint = torch.load(f"{path}/{filename}", map_location=self.device)
        self.model.load_state_dict(checkpoint["model_state"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state"])
        self.train_losses = checkpoint["train_losses"]
        self.val_losses = checkpoint["val_losses"]


def compute_reconstruction_error(model: nn.Module, data: torch.Tensor, device: str) -> np.ndarray:
    model.eval()
    with torch.no_grad():
        data = data.to(device)
        recon, _ = model(data)
        errors = torch.mean((recon - data) ** 2, dim=list(range(1, recon.dim()))).cpu().numpy()
    return errors
