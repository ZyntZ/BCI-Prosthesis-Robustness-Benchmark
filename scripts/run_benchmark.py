"""Run the first-pass BCI robustness benchmark on open MOABB datasets.

Default mode is a dry run so the repository can be inspected without downloading
large EEG files. Use `--download-and-run` to fetch real data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

from moabb.datasets import PhysionetMI, BNCI2014_001
from moabb.paradigms import LeftRightImagery
from moabb.utils import set_download_dir

# Allow running
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bci_robustness.core import evaluate_subject_with_dropout, subject_bootstrap_ci


DATASET_REGISTRY = {
    "PhysionetMI": PhysionetMI,
    "PhysionetMotorImagery": PhysionetMI,
    "BNCI2014_001": BNCI2014_001,
    "BNCI2014-001": BNCI2014_001,
}


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def instantiate_dataset(name: str, subjects: list[int] | None = None):
    if name not in DATASET_REGISTRY:
        raise ValueError(f"Unknown dataset {name!r}. Known: {sorted(DATASET_REGISTRY)}")
    cls = DATASET_REGISTRY[name]
    if cls is PhysionetMI:
        return cls(imagined=True, executed=False, subjects=subjects)
    return cls()


def dry_run(config: dict) -> None:
    print("Dry run only: no EEG data will be downloaded.")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("\nAvailable starter datasets:")
    for key, cls in DATASET_REGISTRY.items():
        try:
            ds = cls(imagined=True, executed=False, subjects=[1]) if cls is PhysionetMI else cls()
            print(f"- {key}: code={ds.code}, subjects={len(ds.subject_list)}")
        except Exception as exc:
            print(f"- {key}: metadata unavailable ({exc})")


def run_real_data(config: dict, dataset_name: str, subjects: list[int], max_subjects: int | None) -> pd.DataFrame:
    set_download_dir(config["moabb_data_dir"])
    dataset = instantiate_dataset(dataset_name, subjects=subjects)
    if subjects:
        subject_list = subjects
    else:
        subject_list = list(dataset.subject_list)
    if max_subjects is not None:
        subject_list = subject_list[:max_subjects]

    paradigm = LeftRightImagery(fmin=8, fmax=32, resample=128)
    dropout_cfg = config["stressors"]["channel_dropout"]
    fractions = [0.0] + [float(x) for x in dropout_cfg["dropout_fractions"]]
    repeats = int(dropout_cfg["repeats_per_fraction"])
    seed = int(config["random_seed"])
    csp_components = int(config["pipelines"][0].get("csp_components", 6))

    all_rows = []
    for subject in subject_list:
        print(f"Loading subject {subject} from {dataset.code}...")
        X, y, metadata = paradigm.get_data(dataset=dataset, subjects=[subject])
        print(f"  X={X.shape}, classes={sorted(set(y))}")
        df = evaluate_subject_with_dropout(
            X=X,
            y=y,
            subject_id=subject,
            dropout_fractions=fractions,
            repeats_per_fraction=repeats,
            random_seed=seed,
            csp_components=csp_components,
        )
        df.insert(0, "dataset", dataset.code)
        all_rows.append(df)
    results = pd.concat(all_rows, ignore_index=True)
    return results


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    # First average folds/repeats
    subj = (
        results.groupby(["dataset", "subject", "dropout_fraction"], as_index=False)
        .agg(roc_auc=("roc_auc", "mean"), balanced_accuracy=("balanced_accuracy", "mean"))
    )
    rows = []
    for (dataset, frac), g in subj.groupby(["dataset", "dropout_fraction"]):
        lo, hi = subject_bootstrap_ci(g["roc_auc"].to_numpy())
        rows.append(
            {
                "dataset": dataset,
                "dropout_fraction": frac,
                "n_subjects": g["subject"].nunique(),
                "mean_roc_auc": g["roc_auc"].mean(),
                "roc_auc_ci_low": lo,
                "roc_auc_ci_high": hi,
                "mean_balanced_accuracy": g["balanced_accuracy"].mean(),
            }
        )
    return pd.DataFrame(rows).sort_values(["dataset", "dropout_fraction"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "benchmark.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Inspect plan without downloading data.")
    parser.add_argument("--download-and-run", action="store_true", help="Download public EEG data and run benchmark.")
    parser.add_argument("--dataset", default="PhysionetMI")
    parser.add_argument("--subjects", type=int, nargs="*", default=[1], help="Subject IDs to run. Default: subject 1 smoke test.")
    parser.add_argument("--max-subjects", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    if args.dry_run or not args.download_and_run:
        dry_run(config)
        return

    results_dir = Path(config["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)
    results = run_real_data(config, args.dataset, args.subjects, args.max_subjects)
    raw_path = results_dir / f"{args.dataset}_dropout_results.csv"
    summary_path = results_dir / f"{args.dataset}_dropout_summary.csv"
    results.to_csv(raw_path, index=False)
    summary = summarize(results)
    summary.to_csv(summary_path, index=False)
    print("\nSubject-level summary:")
    print(summary.to_string(index=False))
    print(f"\nWrote {raw_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
