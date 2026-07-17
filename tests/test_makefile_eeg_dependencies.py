from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_data_targets_require_eeg_dependencies():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    for target in [
        "list-subjects",
        "physionet-full",
        "physionet-full-strict",
        "physionet-full-skip-failed",
        "bnci-full",
    ]:
        assert f"{target}: ensure-eeg" in makefile


def test_eeg_install_uses_same_configured_python():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert '$(PYTHON) -m pip install -e ".[eeg]"' in makefile
    assert '$(PYTHON) -c "import mne, moabb, pyriemann"' in makefile


def test_postprocessing_targets_require_reporting_dependencies():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    for target in ["analyze-dev10", "recommendations-dev10", "analyze-full", "recommendations-full"]:
        assert f"{target}: ensure-reports" in makefile
    assert '$(PYTHON) -m pip install -e ".[reports]"' in makefile
    assert '$(PYTHON) -c "import matplotlib, plotly, seaborn"' in makefile


def test_validation_includes_completed_full_physionet_outputs():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert "validate-results: validate-dev10 validate-bnci validate-physionet-full" in makefile
    assert "PhysionetMI_PhysionetMI_all_csp_lda" in makefile
    assert "PhysionetMI_PhysionetMI_all_riemann_lr" in makefile
