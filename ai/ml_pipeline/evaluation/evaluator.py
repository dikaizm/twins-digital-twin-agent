import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score, accuracy_score,
    roc_auc_score, confusion_matrix, average_precision_score
)
from typing import Dict, Any, Tuple
import pandas as pd


class AnomalyEvaluator:
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.results: Dict[str, Any] = {}

    def compute_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_scores: np.ndarray = None
    ) -> Dict[str, float]:
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0)
        }

        if y_scores is not None and len(np.unique(y_true)) > 1:
            metrics["roc_auc"] = roc_auc_score(y_true, y_scores)
            metrics["avg_precision"] = average_precision_score(y_true, y_scores)

        return metrics

    def evaluate(
        self,
        errors: np.ndarray,
        labels: np.ndarray,
        percentile: float = 95
    ) -> Dict[str, Any]:
        threshold = np.percentile(errors, percentile)
        predictions = (errors > threshold).astype(int)

        metrics = self.compute_metrics(labels, predictions, errors)

        cm = confusion_matrix(labels, predictions)
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

        self.results = {
            "metrics": metrics,
            "threshold": float(threshold),
            "confusion_matrix": {
                "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)
            },
            "percentile": percentile
        }

        return self.results

    def get_summary(self) -> pd.DataFrame:
        if not self.results:
            return pd.DataFrame()

        metrics = self.results.get("metrics", {})
        return pd.DataFrame([metrics])


def evaluate_models(
    isolation_forest_scores: np.ndarray,
    lstm_errors: np.ndarray,
    labels: np.ndarray,
    weights: Tuple[float, float] = (0.4, 0.6)
) -> Dict[str, Any]:
    w_if, w_lstm = weights

    combined_scores = w_if * (-isolation_forest_scores) + w_lstm * lstm_errors
    threshold = np.percentile(combined_scores, 95)
    predictions = (combined_scores > threshold).astype(int)

    evaluator = AnomalyEvaluator(threshold=threshold)
    results = evaluator.compute_metrics(labels, predictions, combined_scores)

    cm = confusion_matrix(labels, predictions)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

    return {
        "metrics": results,
        "threshold": float(threshold),
        "weights": {"isolation_forest": w_if, "lstm": w_lstm},
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
    }
