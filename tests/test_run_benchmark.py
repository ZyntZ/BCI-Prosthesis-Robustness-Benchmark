from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_run_benchmark_module():
    spec = importlib.util.spec_from_file_location(
        "run_benchmark_for_test", ROOT / "scripts" / "run_benchmark.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_set_download_dir_creates_directory_and_sets_mne_config(tmp_path, monkeypatch):
    module = load_run_benchmark_module()
    target = tmp_path / "moabb data"
    calls = []

    module._MOABB_IMPORT_ERROR = None
    fake_mne = types.SimpleNamespace(
        set_config=lambda key, value, set_env: calls.append((key, value, set_env))
    )
    monkeypatch.setitem(sys.modules, "mne", fake_mne)
    module.set_download_dir(target)

    assert target.is_dir()
    assert calls == [("MNE_DATA", str(target.resolve()), False)]


def test_refresh_summaries_preserves_named_regions(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "refresh_benchmark_summaries_for_test", ROOT / "scripts" / "refresh_benchmark_summaries.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    import pandas as pd

    prefix = "demo"
    rows = []
    for region, auc in [("left_motor_strip", 0.6), ("right_motor_strip", 0.8)]:
        rows.append({
            "dataset": "D", "subject": 1, "pipeline": "p", "stressor": "region_dropout",
            "montage": "all_channels", "dropout_fraction": 0.1, "region": region,
            "fold": 1, "repeat": 0, "roc_auc": auc, "balanced_accuracy": auc,
            "brier_score": 0.2, "ece": 0.1, "n_channels": 64, "n_dropped_channels": 6,
        })
    pd.DataFrame(rows).to_csv(tmp_path / f"{prefix}_results.csv", index=False)
    result = module.refresh_summaries(tmp_path, prefix, random_seed=42)
    summary = pd.read_csv(tmp_path / f"{prefix}_subject_summary.csv")
    assert result["n_subject_condition_rows"] == 2
    assert set(summary["region"]) == {"left_motor_strip", "right_motor_strip"}
