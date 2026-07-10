"""Core utilities for BCI robustness benchmark.

No data are bundled here. Functions expect EEG arrays loaded from public datasets
through MOABB/MNE or other documented sources.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.stats import bootstrap
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline

try:
    from mne.decoding import CSP
except Exception as exc:  # pragma: no cover
    CSP = None
    _CSP_IMPORT_ERROR = exc


@dataclass(frozen=True)
class DropoutSpec:
    """Specification for test-time channel dropout stressor."""

    fraction: float
    repeat: int
    random_seed: int


def make_csp_lda(n_components: int = 6, random_state: int = 20260709) -> Pipeline:
    """Create a classical motor-imagery BCI baseline: CSP + LDA.

    This is intentionally not novel. It is a transparent anchor against which
    robustness failures can be quantified.
    """
    if CSP is None:  # pragma: no cover
        raise ImportError(f"mne.decoding.CSP could not be imported: {_CSP_IMPORT_ERROR}")
    return Pipeline(
        steps=[
            ("csp", CSP(n_components=n_components, reg=None, log=True, norm_trace=False)),
            ("lda", LinearDiscriminantAnalysis()),
        ]
    )


def apply_channel_dropout(
    X: np.ndarray,
    fraction: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Zero a random subset of channels in all epochs.

    Parameters
    ----------
    X:
        EEG array with shape (epochs, channels, samples).
    fraction:
        Fraction of channels to zero. Must be in [0, 1).
    rng:
        NumPy random generator.

    Returns
    -------
    X_corrupted, dropped_channel_indices
    """
    if X.ndim != 3:
        raise ValueError(f"Expected X with 3 dimensions; got shape {X.shape}")
    if not (0 <= fraction < 1):
        raise ValueError("fraction must be in [0, 1)")
    n_channels = X.shape[1]
    n_drop = int(round(fraction * n_channels))
    X2 = X.copy()
    if n_drop == 0:
        return X2, np.array([], dtype=int)
    dropped = np.sort(rng.choice(n_channels, size=n_drop, replace=False))
    X2[:, dropped, :] = 0.0
    return X2, dropped


def _binary_scores(estimator, X_test: np.ndarray) -> np.ndarray:
    """Return continuous scores for binary ROC-AUC."""
    if hasattr(estimator, "predict_proba"):
        return estimator.predict_proba(X_test)[:, 1]
    if hasattr(estimator, "decision_function"):
        return estimator.decision_function(X_test)
    return estimator.predict(X_test)


def evaluate_subject_with_dropout(
    X: np.ndarray,
    y: np.ndarray,
    subject_id: str | int,
    dropout_fractions: Iterable[float] = (0.0, 0.1, 0.2, 0.3, 0.5),
    repeats_per_fraction: int = 20,
    n_splits: int = 5,
    random_seed: int = 20260709,
    csp_components: int = 6,
) -> pd.DataFrame:
    """Evaluate clean and test-time channel-dropout performance for one subject.

    The training fold is never corrupted. Each test fold is evaluated clean and
    under repeated random channel-dropout masks. This estimates deployment
    fragility rather than data augmentation benefit.
    """
    X = np.asarray(X)
    y = np.asarray(y)
    if len(np.unique(y)) != 2:
        raise ValueError("This starter evaluator expects exactly two classes")
    if X.shape[0] != y.shape[0]:
        raise ValueError("X and y have inconsistent numbers of epochs")

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_seed)
    rows = []
    for fold, (train_idx, test_idx) in enumerate(cv.split(X, y), start=1):
        clf = make_csp_lda(n_components=csp_components, random_state=random_seed)
        clf.fit(X[train_idx], y[train_idx])
        y_test = y[test_idx]
        for fraction in dropout_fractions:
            n_repeats = 1 if fraction == 0 else repeats_per_fraction
            for repeat in range(n_repeats):
                rng = np.random.default_rng(random_seed + 1000 * fold + 100 * repeat + int(100 * fraction))
                X_eval, dropped = apply_channel_dropout(X[test_idx], float(fraction), rng)
                y_pred = clf.predict(X_eval)
                y_score = _binary_scores(clf, X_eval)
                try:
                    auc = roc_auc_score(y_test, y_score)
                except ValueError:
                    auc = np.nan
                rows.append(
                    {
                        "subject": subject_id,
                        "fold": fold,
                        "dropout_fraction": float(fraction),
                        "repeat": repeat,
                        "n_dropped_channels": int(len(dropped)),
                        "balanced_accuracy": balanced_accuracy_score(y_test, y_pred),
                        "roc_auc": auc,
                    }
                )
    return pd.DataFrame(rows)


def subject_bootstrap_ci(values: np.ndarray, confidence_level: float = 0.95, random_seed: int = 20260709) -> tuple[float, float]:
    """Bootstrap confidence interval for a mean over subjects.

    Use this only when values are subject-level summary statistics, not folds;
    folds from the same subject are not independent.
    """
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 2:
        return (np.nan, np.nan)
    res = bootstrap(
        (values,),
        np.mean,
        confidence_level=confidence_level,
        n_resamples=2000,
        random_state=random_seed,
        method="BCa",
    )
    return float(res.confidence_interval.low), float(res.confidence_interval.high)
