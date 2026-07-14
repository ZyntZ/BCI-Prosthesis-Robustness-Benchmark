import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_results", ROOT / "scripts" / "validate_results.py")
validate_results = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_results)


def test_existing_dev10_results_pass_error_level_validation():
    report, summary = validate_results.validate_prefix(ROOT / "results", "PhysionetMI_dev10")
    assert summary["n_failed_errors"] == 0
    assert summary["n_checks"] >= 10
    assert {"fold_results_roc_auc_range", "subject_summary_key_match", "clean_baseline_present"}.issubset(set(report["check"]))


def test_crosscheck_detects_subject_summary_metric_mismatch():
    results = pd.DataFrame(
        {
            "dataset": ["D", "D"],
            "subject": [1, 1],
            "pipeline": ["p", "p"],
            "stressor": ["clean", "clean"],
            "montage": ["all_channels", "all_channels"],
            "dropout_fraction": [0.0, 0.0],
            "fold": [1, 2],
            "repeat": [0, 0],
            "roc_auc": [0.7, 0.9],
            "balanced_accuracy": [0.6, 0.8],
            "n_channels": [8, 8],
            "n_dropped_channels": [0, 0],
        }
    )
    subject = pd.DataFrame(
        {
            "dataset": ["D"],
            "subject": [1],
            "pipeline": ["p"],
            "stressor": ["clean"],
            "montage": ["all_channels"],
            "dropout_fraction": [0.0],
            "roc_auc": [0.1],
            "balanced_accuracy": [0.7],
            "n_channels": [8],
            "n_dropped_channels": [0],
        }
    )
    rows = []
    validate_results.validate_subject_summary_against_results(results, subject, rows)
    out = pd.DataFrame(rows)
    mismatch = out.loc[out["check"].eq("subject_summary_roc_auc_mean_match")].iloc[0]
    assert not mismatch["passed"]
    assert mismatch["severity"] == "error"
