import yaml
import argparse
import numpy as np
import torch
from pathlib import Path
from rich.console import Console
from rich.table import Table

from data_processing.preprocessor import DataPreprocessor, create_sequences
from data_processing.dataset import create_dataloaders
from models.isolation_forest import IsolationForestDetector
from models.lstm_autoencoder import LSTMAutoencoder, create_model
from training.trainer import Trainer, compute_reconstruction_error
from evaluation.evaluator import AnomalyEvaluator, evaluate_models


console = Console()


class Pipeline:
    def __init__(self, config_path: str = "configs/train_config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.preprocessor = DataPreprocessor(self.config["data"]["scaler_type"])

    def load_data(self) -> dict:
        console.print("[bold blue]Loading data...[/bold blue]")

        base = "data/raw"
        data = {
            "train": np.load(f"{base}/train_data.npy"),
            "val": np.load(f"{base}/val_data.npy"),
            "test": np.load(f"{base}/test_data.npy")
        }
        labels = {
            "train": np.load(f"{base}/train_labels.npy"),
            "val": np.load(f"{base}/val_labels.npy"),
            "test": np.load(f"{base}/test_labels.npy")
        }

        console.print(f"  Train: {len(data['train'])} samples")
        console.print(f"  Val: {len(data['val'])} samples")
        console.print(f"  Test: {len(data['test'])} samples")

        return data, labels

    def preprocess(self, data: dict) -> dict:
        console.print("[bold blue]Preprocessing data...[/bold blue]")

        all_data = np.vstack([data["train"], data["val"]])
        self.preprocessor.fit(all_data)

        processed = {
            "train": self.preprocessor.transform(data["train"]),
            "val": self.preprocessor.transform(data["val"]),
            "test": self.preprocessor.transform(data["test"])
        }

        return processed

    def train_isolation_forest(self, X_train: np.ndarray) -> IsolationForestDetector:
        console.print("[bold blue]Training Isolation Forest...[/bold blue]")

        if_config = self.config["isolation_forest"]
        detector = IsolationForestDetector(if_config)
        detector.fit(X_train)

        return detector

    def train_lstm(self, train_loader, val_loader) -> tuple[Trainer, LSTMAutoencoder]:
        console.print("[bold blue]Training LSTM Autoencoder...[/bold blue]")

        lstm_config = self.config["lstm"]
        model = create_model(lstm_config["input_dim"], lstm_config)

        trainer = Trainer(model, self.device)
        trainer.compile(lr=lstm_config["lr"])

        history = trainer.fit(
            train_loader,
            val_loader,
            epochs=lstm_config["epochs"],
            early_stopping_patience=lstm_config["early_stopping_patience"],
            checkpoint_dir=self.config["training"]["checkpoint_dir"]
        )

        return trainer, model

    def evaluate(
        self,
        detector: IsolationForestDetector,
        lstm_trainer: Trainer,
        data: dict,
        labels: dict
    ) -> dict:
        console.print("[bold blue]Evaluating models...[/bold blue]")

        if_scores = detector.score(data["test"])
        lstm_errors = compute_reconstruction_error(
            lstm_trainer.model,
            torch.FloatTensor(data["test"]),
            self.device
        )

        ensemble_results = evaluate_models(
            if_scores, lstm_errors, labels["test"],
            weights=(self.config["ensemble"]["weights"]["isolation_forest"],
                     self.config["ensemble"]["weights"]["lstm"])
        )

        return ensemble_results

    def print_results(self, results: dict):
        table = Table(title="Evaluation Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        for key, value in results["metrics"].items():
            table.add_row(key, f"{value:.4f}")

        table.add_row("threshold", f"{results['threshold']:.4f}")
        table.add_row("weights", f"IF={results['weights']['isolation_forest']}, LSTM={results['weights']['lstm']}")

        console.print(table)

    def run(self):
        console.print("[bold green]Starting ML Pipeline...[/bold green]\n")

        data, labels = self.load_data()
        processed = self.preprocess(data)

        loaders = create_dataloaders(
            processed["train"], processed["val"], processed["test"],
            batch_size=self.config["lstm"]["batch_size"],
            labels=labels
        )

        detector = self.train_isolation_forest(processed["train"])
        trainer, model = self.train_lstm(loaders["train"], loaders["val"])

        results = self.evaluate(detector, trainer, processed, labels)
        self.print_results(results)

        console.print("\n[bold green]Pipeline complete![/bold green]")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["train", "evaluate", "run"])
    parser.add_argument("--config", default="configs/train_config.yaml")
    parser.add_argument("--model", default="models")
    args = parser.parse_args()

    pipeline = Pipeline(args.config)

    if args.command == "run":
        pipeline.run()
    elif args.command == "train":
        console.print("[yellow]Generating mock data first...[/yellow]")
        from data_processing.mock_data import MockDataGenerator
        MockDataGenerator().generate_dataset()
        pipeline.run()


if __name__ == "__main__":
    main()
