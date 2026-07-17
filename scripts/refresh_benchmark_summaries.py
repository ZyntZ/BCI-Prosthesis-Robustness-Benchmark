#!/usr/bin/env python3
"""Rebuild subject and population summaries from an existing fold-level results CSV."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bci_robustness.core import population_summary, subject_level_summary


def refresh_summaries(results_dir: Path, prefix: str, random_seed: int = 42) -> dict[str, object]:
    raw_path = results_dir / f"{prefix}_results.csv"
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)
    results = pd.read_csv(raw_path)
    required = {"dataset", "subject", "pipeline", "stressor", "montage", "dropout_fraction", "roc_auc", "balanced_accuracy", "n_channels"}
    missing = sorted(required - set(results.columns))
    if missing:
        raise ValueError(f"{raw_path} is missing required columns: {missing}")
    subject = subject_level_summary(results)
    population = population_summary(results, random_seed=random_seed)
    subject_path = results_dir / f"{prefix}_subject_summary.csv"
    population_path = results_dir / f"{prefix}_population_summary.csv"
    subject.to_csv(subject_path, index=False)
    population.to_csv(population_path, index=False)
    return {
        "prefix": prefix,
        "source": str(raw_path),
        "n_fold_rows": int(len(results)),
        "n_subjects": int(subject["subject"].nunique()),
        "n_subject_condition_rows": int(len(subject)),
        "subject_summary": str(subject_path),
        "population_summary": str(population_path),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", type=Path, default=Path("results"))
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--random-seed", type=int, default=42)
    args = ap.parse_args()
    print(json.dumps(refresh_summaries(args.results_dir, args.prefix, args.random_seed), indent=2))


if __name__ == "__main__":
    main()
