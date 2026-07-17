import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("final_statistics", ROOT / "scripts" / "final_statistics.py")
final_statistics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(final_statistics)


def test_intervention_classes_include_ok_dev_not_false_high_priority():
    wide = pd.DataFrame(
        {
            "subject": [1, 2, 3, 4, 5],
            "clean_auc": [0.70, 0.70, 0.55, 0.55, 0.80],
            "auc_dropout_0.5": [0.65, 0.45, 0.50, 0.50, 0.55],
            "auc_motor_core": [0.66, 0.62, 0.65, 0.50, 0.57],
            "auc_motor_extended": [0.64, 0.58, 0.61, 0.52, 0.58],
        }
    )
    out = final_statistics.intervention_classes(wide, clean_thr=0.60, fail_thr=0.60)
    by_subject = dict(zip(out["subject"], out["intervention_class"]))

    assert by_subject[1] == "C_ok_dev"
    assert by_subject[2] == "A_high"
    assert by_subject[3] == "B_rescue_candidate"
    assert by_subject[4] == "D_low_clean"
    assert by_subject[5] == "B_fragile"


def test_intervention_class_rates_report_c_ok_dev():
    classes = pd.DataFrame(
        {
            "intervention_class": ["A_high", "C_ok_dev", "D_low_clean"],
            "clean_working": [True, True, False],
            "dropout_failure_at_50pct": [True, False, False],
            "montage_rescue": [True, False, False],
        }
    )
    rates = final_statistics.intervention_class_rates(classes)
    assert "class_C_ok_dev" in set(rates["metric"])
    row = rates.loc[rates["metric"] == "class_C_ok_dev"].iloc[0]
    assert row["numerator"] == 1
    assert row["denominator"] == 3



def _subject_summary_with_all_stressors() -> pd.DataFrame:
    rows = []
    for subject, clean in [(1, 0.80), (2, 0.70), (3, 0.75)]:
        common = {"dataset": "D", "subject": subject, "pipeline": "p", "montage": "all_channels"}
        rows.extend([
            {**common, "stressor": "clean", "dropout_fraction": 0.0, "roc_auc": clean, "balanced_accuracy": clean - 0.05},
            {**common, "stressor": "channel_dropout", "dropout_fraction": 0.5, "roc_auc": clean - 0.15, "balanced_accuracy": clean - 0.20},
            {**common, "stressor": "region_dropout", "dropout_fraction": 0.3, "roc_auc": clean - 0.10, "balanced_accuracy": clean - 0.15},
            {**common, "stressor": "cross_session", "dropout_fraction": 0.0, "roc_auc": clean - 0.05, "balanced_accuracy": clean - 0.10},
            {**common, "stressor": "reduced_montage", "montage": "motor_core", "dropout_fraction": 0.0, "roc_auc": clean - 0.02, "balanced_accuracy": clean - 0.07},
        ])
    return pd.DataFrame(rows)


def test_wide_auc_and_paired_sensitivity_include_all_stressors():
    wide = final_statistics.wide_auc(_subject_summary_with_all_stressors())
    expected = {"auc_dropout_0.5", "auc_region_dropout_0.3", "auc_cross_session_0", "auc_motor_core"}
    assert expected.issubset(wide.columns)
    paired = final_statistics.paired_sensitivity(wide)
    assert expected == {f"auc_{condition}" for condition in paired["condition"]}


def test_mixed_effects_separates_all_conditions_from_dropout_dose():
    out = final_statistics.mixed_effects(_subject_summary_with_all_stressors())
    assert set(out["model_id"]) == {"all_conditions", "channel_dropout_dose"}
    dose = out[out["model_id"] == "channel_dropout_dose"]
    assert set(dose["model"]) == {"roc_auc ~ dropout_fraction"}
    assert "dropout_fraction" in set(dose["term"].dropna())
