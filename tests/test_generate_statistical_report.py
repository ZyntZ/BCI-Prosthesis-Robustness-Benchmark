import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("generate_statistical_report", ROOT / "scripts" / "generate_statistical_report.py")
generate_statistical_report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate_statistical_report)


def test_generate_statistical_report_on_existing_dev10_subject_summary():
    subj = generate_statistical_report.load_subject_summary(ROOT / "results", "PhysionetMI_dev10")
    audit = generate_statistical_report.methods_audit(subj)
    paired = generate_statistical_report.paired_condition_effects(subj)
    slopes = generate_statistical_report.channel_dropout_slopes(subj)
    slopes_pop = generate_statistical_report.slope_population_summary(slopes)
    table = generate_statistical_report.report_table(paired)

    assert not audit.empty
    assert "duplicate_subject_condition_rows" in set(audit["check"])
    assert not paired.empty
    assert {"roc_auc", "balanced_accuracy"}.issubset(set(paired["metric"]))
    assert not slopes.empty
    assert not slopes_pop.empty
    assert not table.empty
    assert table["condition"].str.contains("channel_dropout").any()


def test_condition_labels_are_stable_for_existing_rows():
    subj = generate_statistical_report.load_subject_summary(ROOT / "results", "PhysionetMI_dev10")
    labelled = generate_statistical_report.add_condition(subj)
    assert "clean_all_channels" in set(labelled["condition"])
    assert labelled.loc[labelled["stressor"].eq("reduced_montage"), "condition"].str.startswith("reduced_montage_").all()


def test_extended_statistical_tables_include_effects_sensitivity_and_flags():
    subj = generate_statistical_report.load_subject_summary(ROOT / "results", "PhysionetMI_dev10")
    paired = generate_statistical_report.paired_condition_effects(subj)
    effects = generate_statistical_report.effect_size_interpretation(paired)
    sensitivity = generate_statistical_report.sensitivity_summary(paired)
    flags = generate_statistical_report.overclaim_flags(subj, paired, "PhysionetMI_dev10")

    assert not effects.empty
    assert {"median_delta_condition_minus_clean", "cohens_dz_magnitude", "evidence_flag"}.issubset(effects.columns)
    assert not sensitivity.empty
    assert {"primary", "secondary"}.issubset(set(sensitivity.loc[sensitivity["available"], "role"]))
    assert not flags.empty
    assert "development_subset_prefix" in set(flags["flag"])
    assert flags.loc[flags["flag"].eq("development_subset_prefix"), "triggered"].iloc[0]


def test_statistical_report_renderers_do_not_require_optional_pandas_styler_dependencies(tmp_path):
    table = generate_statistical_report.report_table(
        generate_statistical_report.paired_condition_effects(
            generate_statistical_report.load_subject_summary(ROOT / "results", "PhysionetMI_dev10")
        )
    ).head(2)
    out = tmp_path / "table.tex"
    generate_statistical_report.write_latex_table(table, out)
    text = out.read_text()
    assert "\\begin{tabular}" in text
    assert "roc\\_auc" in text or "balanced\\_accuracy" in text

    md = generate_statistical_report.dataframe_to_markdown(table)
    assert md.startswith("| ")
    assert "---" in md
