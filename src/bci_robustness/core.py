"""Core utilities for the BCI robustness benchmark.

No data are bundled here. Functions expect EEG arrays loaded from public datasets
through MOABB/MNE or other documented sources.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy.stats import bootstrap
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
    """Specification for a test-time channel-dropout stressor."""

    fraction: float
    repeat: int
    random_seed: int


def make_csp_lda(n_components: int = 6, random_state: int = 20260709) -> Pipeline:
    """Create a classical motor-imagery BCI baseline: CSP + LDA."""
    if CSP is None:  # pragma: no cover
        raise ImportError(f"mne.decoding.CSP could not be imported: {_CSP_IMPORT_ERROR}")
    return Pipeline(
        steps=[
            ("csp", CSP(n_components=n_components, reg=None, log=True, norm_trace=False)),
            ("lda", LinearDiscriminantAnalysis()),
        ]
    )


def apply_channel_dropout(X: np.ndarray, fraction: float, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Zero a random subset of channels in all epochs.

    X must have shape (epochs, channels, samples). Training data should not be
    corrupted when this function is used to model deployment-time channel loss.
    """
    X = np.asarray(X)
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


def channel_indices(channel_names: Sequence[str], wanted: Sequence[str]) -> list[int]:
    """Return channel indices for a requested montage, preserving requested order."""
    name_to_idx = {name: idx for idx, name in enumerate(channel_names)}
    missing = [name for name in wanted if name not in name_to_idx]
    if missing:
        raise ValueError(f"Requested channels are absent from dataset: {missing}")
    return [name_to_idx[name] for name in wanted]


def select_channels(X: np.ndarray, channel_names: Sequence[str], wanted: Sequence[str]) -> tuple[np.ndarray, list[str], list[int]]:
    """Select a reduced montage from an EEG tensor."""
    idx = channel_indices(channel_names, wanted)
    return np.asarray(X)[:, idx, :], [channel_names[i] for i in idx], idx


def _binary_scores(estimator, X_test: np.ndarray) -> np.ndarray:
    """Return continuous scores for binary ROC-AUC."""
    if hasattr(estimator, "predict_proba"):
        return estimator.predict_proba(X_test)[:, 1]
    if hasattr(estimator, "decision_function"):
        return estimator.decision_function(X_test)
    return estimator.predict(X_test)


def _score_fold(estimator, X_test: np.ndarray, y_test: np.ndarray) -> tuple[float, float]:
    y_pred = estimator.predict(X_test)
    y_score = _binary_scores(estimator, X_test)
    try:
        auc = roc_auc_score(y_test, y_score)
    except ValueError:
        auc = np.nan
    return float(auc), float(balanced_accuracy_score(y_test, y_pred))


def evaluate_subject_with_dropout(
    X: np.ndarray,
    y: np.ndarray,
    subject_id: str | int,
    dropout_fractions: Iterable[float] = (0.0, 0.1, 0.2, 0.3, 0.5),
    repeats_per_fraction: int = 20,
    n_splits: int = 5,
    random_seed: int = 20260709,
    csp_components: int = 6,
    pipeline_name: str = "csp_lda",
    montage_name: str = "all_channels",
    n_channels: int | None = None,
) -> pd.DataFrame:
    """Evaluate clean and test-time channel-dropout performance for one subject.

    Folds/repeats are technical resampling units. For inference, collapse these
    rows to subject-level summaries before computing confidence intervals or p-values.
    """
    X = np.asarray(X)
    y = np.asarray(y)
    if len(np.unique(y)) != 2:
        raise ValueError("This evaluator expects exactly two classes")
    if X.shape[0] != y.shape[0]:
        raise ValueError("X and y have inconsistent numbers of epochs")
    if n_channels is None:
        n_channels = X.shape[1]

    _, counts = np.unique(y, return_counts=True)
    n_splits_eff = min(int(n_splits), int(counts.min()))
    if n_splits_eff < 2:
        raise ValueError("Need at least two samples per class for cross-validation")

    cv = StratifiedKFold(n_splits=n_splits_eff, shuffle=True, random_state=random_seed)
    rows = []
    for fold, (train_idx, test_idx) in enumerate(cv.split(X, y), start=1):
        clf = make_csp_lda(n_components=min(csp_components, X.shape[1]), random_state=random_seed)
        clf.fit(X[train_idx], y[train_idx])
        y_test = y[test_idx]
        for fraction in dropout_fractions:
            fraction = float(fraction)
            n_repeats = 1 if fraction == 0.0 else repeats_per_fraction
            for repeat in range(n_repeats):
                rng = np.random.default_rng(random_seed + 1000 * fold + 100 * repeat + int(100 * fraction))
                X_eval, dropped = apply_channel_dropout(X[test_idx], fraction, rng)
                auc, bal_acc = _score_fold(clf, X_eval, y_test)
                rows.append(
                    {
                        "subject": subject_id,
                        "pipeline": pipeline_name,
                        "stressor": "channel_dropout" if fraction > 0 else "clean",
                        "montage": montage_name,
                        "fold": fold,
                        "dropout_fraction": fraction,
                        "repeat": repeat,
                        "n_channels": int(n_channels),
                        "n_dropped_channels": int(len(dropped)),
                        "balanced_accuracy": bal_acc,
                        "roc_auc": auc,
                    }
                )
    return pd.DataFrame(rows)


def evaluate_subject_reduced_montages(
    X: np.ndarray,
    y: np.ndarray,
    channel_names: Sequence[str],
    subject_id: str | int,
    montages: dict[str, Sequence[str]],
    n_splits: int = 5,
    random_seed: int = 20260709,
    csp_components: int = 6,
    pipeline_name: str = "csp_lda",
) -> pd.DataFrame:
    """Evaluate clean performance on named reduced montages.

    Unlike random channel dropout, training and testing both use the same smaller
    channel set. This approximates a cheaper or more wearable electrode montage.
    """
    frames = []
    for montage_name, wanted in montages.items():
        X_sel, selected_names, _ = select_channels(X, channel_names, wanted)
        df = evaluate_subject_with_dropout(
            X_sel,
            y,
            subject_id=subject_id,
            dropout_fractions=(0.0,),
            repeats_per_fraction=1,
            n_splits=n_splits,
            random_seed=random_seed,
            csp_components=min(csp_components, X_sel.shape[1]),
            pipeline_name=pipeline_name,
            montage_name=montage_name,
            n_channels=X_sel.shape[1],
        )
        df["stressor"] = "reduced_montage"
        df["selected_channels"] = ",".join(selected_names)
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def subject_level_summary(results: pd.DataFrame) -> pd.DataFrame:
    """Average folds/repeats within subject before population summaries."""
    group_cols = ["dataset", "subject", "pipeline", "stressor", "montage", "dropout_fraction"]
    present = [c for c in group_cols if c in results.columns]
    return (
        results.groupby(present, as_index=False)
        .agg(
            roc_auc=("roc_auc", "mean"),
            balanced_accuracy=("balanced_accuracy", "mean"),
            n_channels=("n_channels", "first"),
            n_dropped_channels=("n_dropped_channels", "mean"),
        )
    )


def subject_bootstrap_ci(
    values: np.ndarray,
    confidence_level: float = 0.95,
    random_seed: int = 20260709,
    n_resamples: int = 2000,
) -> tuple[float, float]:
    """Bootstrap confidence interval for a mean over subjects."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 2:
        return (np.nan, np.nan)
    res = bootstrap(
        (values,),
        np.mean,
        confidence_level=confidence_level,
        n_resamples=n_resamples,
        random_state=random_seed,
        method="BCa",
    )
    return float(res.confidence_interval.low), float(res.confidence_interval.high)


def population_summary(results: pd.DataFrame, random_seed: int = 20260709) -> pd.DataFrame:
    """Population summary after collapsing to one row per subject/condition."""
    subj = subject_level_summary(results)
    group_cols = ["dataset", "pipeline", "stressor", "montage", "dropout_fraction"]
    rows = []
    for keys, g in subj.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        lo, hi = subject_bootstrap_ci(g["roc_auc"].to_numpy(), random_seed=random_seed)
        bal_lo, bal_hi = subject_bootstrap_ci(g["balanced_accuracy"].to_numpy(), random_seed=random_seed)
        row = dict(zip(group_cols, keys))
        row.update(
            {
                "n_subjects": int(g["subject"].nunique()),
                "mean_roc_auc": float(g["roc_auc"].mean()),
                "roc_auc_ci_low": lo,
                "roc_auc_ci_high": hi,
                "mean_balanced_accuracy": float(g["balanced_accuracy"].mean()),
                "balanced_accuracy_ci_low": bal_lo,
                "balanced_accuracy_ci_high": bal_hi,
                "mean_n_channels": float(g["n_channels"].mean()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(group_cols).reset_index(drop=True)
