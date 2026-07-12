#!/usr/bin/env python3
"""Run BCI robustness benchmarks on open MOABB datasets.

This version is resumable at the subject level and supports two stressors:
1. test-time random channel dropout;
2. reduced electrode montages trained/tested on smaller channel sets.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

from moabb.datasets import BNCI2014_001, PhysionetMI
from moabb.paradigms import LeftRightImagery
from moabb.utils import set_download_dir

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bci_robustness.core import (
    evaluate_subject_cross_session,
    evaluate_subject_reduced_montages,
    evaluate_subject_region_dropout,
    evaluate_subject_with_dropout,
    population_summary,
    subject_level_summary,
)

DATASET_REGISTRY = {
    "PhysionetMI": PhysionetMI,
    "PhysionetMotorImagery": PhysionetMI,
    "BNCI2014_001": BNCI2014_001,
    "BNCI2014-001": BNCI2014_001,
}


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_config_paths(config: dict) -> dict:
    """Resolve repository-relative paths so scripts can be run from any cwd."""
    config = dict(config)
    for key in ["moabb_data_dir", "results_dir"]:
        if key in config:
            value = Path(config[key])
            if not value.is_absolute():
                config[key] = str((ROOT / value).resolve())
    return config


def instantiate_dataset(name: str, subjects: list[int] | None = None):
    if name not in DATASET_REGISTRY:
        raise ValueError(f"Unknown dataset {name!r}. Known: {sorted(DATASET_REGISTRY)}")
    cls = DATASET_REGISTRY[name]
    if cls is PhysionetMI:
        return cls(imagined=True, executed=False, subjects=subjects)
    return cls()


def config_montages(config: dict) -> dict[str, list[str]]:
    reduced_cfg = config.get("stressors", {}).get("reduced_montage", {})
    montages = {}
    for item in reduced_cfg.get("montages", []):
        montages[item["name"]] = list(item["channels"])
    return montages


def pipeline_config(config: dict, pipeline_name: str) -> dict:
    """Return the pipeline configuration by name, or an empty dict if absent."""
    for item in config.get("pipelines", []):
        if item.get("name") == pipeline_name:
            return item
    return {}


def available_subjects(dataset_name: str, config: dict) -> list[int]:
    """List subjects available through the MOABB dataset wrapper without loading EEG arrays."""
    set_download_dir(config["moabb_data_dir"])
    ds = instantiate_dataset(dataset_name, subjects=None)
    return list(ds.subject_list)


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


def run_one_subject(
    dataset,
    paradigm,
    subject: int,
    config: dict,
    include_reduced_montage: bool,
    include_region_dropout: bool = False,
    include_cross_session: bool = False,
    pipeline_name: str = "csp_lda",
) -> pd.DataFrame:
    seed = int(config["random_seed"])
    dropout_cfg = config["stressors"]["channel_dropout"]
    fractions = [0.0] + [float(x) for x in dropout_cfg["dropout_fractions"]]
    repeats = int(dropout_cfg["repeats_per_fraction"])
    csp_components = int(pipeline_config(config, pipeline_name).get("csp_components", 6))

    epochs, y, metadata = paradigm.get_data(dataset=dataset, subjects=[subject], return_epochs=True)
    X = epochs.get_data(copy=True)
    channel_names = list(epochs.ch_names)
    print(f"  X={X.shape}, classes={sorted(set(y))}, channels={len(channel_names)}")

    frames = []
    dropout = evaluate_subject_with_dropout(
        X=X,
        y=y,
        subject_id=subject,
        dropout_fractions=fractions,
        repeats_per_fraction=repeats,
        random_seed=seed,
        csp_components=csp_components,
        pipeline_name=pipeline_name,
        montage_name="all_channels",
        n_channels=X.shape[1],
    )
    frames.append(dropout)

    if include_reduced_montage and config.get("stressors", {}).get("reduced_montage", {}).get("enabled", False):
        montages = config_montages(config)
        reduced = evaluate_subject_reduced_montages(
            X=X,
            y=y,
            channel_names=channel_names,
            subject_id=subject,
            montages=montages,
            random_seed=seed,
            csp_components=csp_components,
            pipeline_name=pipeline_name,
        )
        frames.append(reduced)

    if include_region_dropout:
        region_cfg = config.get("stressors", {}).get("region_dropout", {})
        region_names = region_cfg.get("regions", ["left_motor_strip", "midline_motor_strip", "right_motor_strip"])
        region = evaluate_subject_region_dropout(
            X=X,
            y=y,
            channel_names=channel_names,
            subject_id=subject,
            region_names=region_names,
            random_seed=seed,
            csp_components=csp_components,
            pipeline_name=pipeline_name,
        )
        frames.append(region)

    if include_cross_session and config.get("stressors", {}).get("cross_session", {}).get("enabled", False):
        cross = evaluate_subject_cross_session(
            X=X,
            y=y,
            metadata=metadata,
            subject_id=subject,
            random_seed=seed,
            csp_components=csp_components,
            pipeline_name=pipeline_name,
        )
        if not cross.empty:
            frames.append(cross)

    out = pd.concat(frames, ignore_index=True)
    out.insert(0, "dataset", dataset.code)
    return out


def run_real_data(
    config: dict,
    dataset_name: str,
    subjects: list[int],
    max_subjects: int | None,
    include_reduced_montage: bool,
    include_region_dropout: bool,
    include_cross_session: bool,
    pipeline_name: str,
    overwrite: bool,
) -> pd.DataFrame:
    set_download_dir(config["moabb_data_dir"])
    dataset = instantiate_dataset(dataset_name, subjects=subjects if subjects else None)
    subject_list = subjects if subjects else list(dataset.subject_list)
    if max_subjects is not None:
        subject_list = subject_list[:max_subjects]

    paradigm = LeftRightImagery(fmin=8, fmax=32, resample=128)
    checkpoint_dir = Path(config["results_dir"]) / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    all_rows = []
    for subject in subject_list:
        ckpt = checkpoint_dir / f"{dataset_name}_{pipeline_name}_subject-{subject:03d}_robustness.csv"
        if ckpt.exists() and not overwrite:
            print(f"Reusing checkpoint: {ckpt}")
            df = pd.read_csv(ckpt)
        else:
            print(f"Loading subject {subject} from {dataset.code}...")
            df = run_one_subject(dataset, paradigm, subject, config, include_reduced_montage, include_region_dropout, include_cross_session, pipeline_name)
            df.to_csv(ckpt, index=False)
            print(f"  wrote checkpoint {ckpt}")
        all_rows.append(df)
    return pd.concat(all_rows, ignore_index=True)


def write_outputs(results: pd.DataFrame, config: dict, dataset_name: str, suffix: str) -> tuple[Path, Path, Path]:
    results_dir = Path(config["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)
    raw_path = results_dir / f"{dataset_name}_{suffix}_results.csv"
    subject_path = results_dir / f"{dataset_name}_{suffix}_subject_summary.csv"
    summary_path = results_dir / f"{dataset_name}_{suffix}_population_summary.csv"
    results.to_csv(raw_path, index=False)
    subj = subject_level_summary(results)
    subj.to_csv(subject_path, index=False)
    summary = population_summary(results, random_seed=int(config["random_seed"]))
    summary.to_csv(summary_path, index=False)
    return raw_path, subject_path, summary_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "benchmark.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Inspect plan without downloading data.")
    parser.add_argument("--download-and-run", action="store_true", help="Download public EEG data and run benchmark.")
    parser.add_argument("--dataset", default="PhysionetMI")
    parser.add_argument("--subjects", type=int, nargs="*", default=None, help="Subject IDs to run. If omitted, run all subjects exposed by MOABB for the dataset.")
    parser.add_argument("--max-subjects", type=int, default=None)
    parser.add_argument("--include-reduced-montage", action="store_true", help="Run reduced montage stressors from config.")
    parser.add_argument("--include-region-dropout", action="store_true", help="Run named region dropout stressors from config/core defaults.")
    parser.add_argument("--include-cross-session", action="store_true", help="Run train-first-session/test-later-session evaluation when MOABB metadata contain sessions.")
    parser.add_argument("--list-subjects", action="store_true", help="Print available MOABB subject IDs for the dataset and exit.")
    parser.add_argument("--pipeline", default="csp_lda", choices=["csp_lda", "riemann_lr", "tangent_space_lr"], help="Decoder pipeline to benchmark.")
    parser.add_argument("--overwrite", action="store_true", help="Recompute existing subject checkpoints.")
    parser.add_argument("--suffix", default="robustness", help="Output filename suffix.")
    args = parser.parse_args()

    config = normalize_config_paths(load_config(args.config))
    if args.list_subjects:
        print(json.dumps({"dataset": args.dataset, "subjects": available_subjects(args.dataset, config)}, indent=2))
        return
    if args.dry_run or not args.download_and_run:
        dry_run(config)
        return

    results = run_real_data(
        config=config,
        dataset_name=args.dataset,
        subjects=args.subjects,
        max_subjects=args.max_subjects,
        include_reduced_montage=args.include_reduced_montage,
        include_region_dropout=args.include_region_dropout,
        include_cross_session=args.include_cross_session,
        pipeline_name=args.pipeline,
        overwrite=args.overwrite,
    )
    raw_path, subject_path, summary_path = write_outputs(results, config, args.dataset, args.suffix)
    print("\nPopulation summary:")
    print(pd.read_csv(summary_path).to_string(index=False))
    print(f"\nWrote {raw_path}")
    print(f"Wrote {subject_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
