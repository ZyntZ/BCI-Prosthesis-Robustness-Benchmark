import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAMES = [
    "analyze_robustness.py",
    "build_release_archive.py",
    "build_release_manifest.py",
    "final_statistics.py",
    "generate_methods_figures.py",
    "generate_statistical_report.py",
    "recommend_interventions.py",
    "run_benchmark.py",
    "validate_results.py",
]
FIGURE_PREFIX = "BNCI2014-001_BNCI2014_001_all_riemann_lr"

SPEC_ARCHIVE = importlib.util.spec_from_file_location("build_release_archive", ROOT / "scripts" / "build_release_archive.py")
build_release_archive = importlib.util.module_from_spec(SPEC_ARCHIVE)
SPEC_ARCHIVE.loader.exec_module(build_release_archive)

SPEC_FIGURES = importlib.util.spec_from_file_location("generate_methods_figures", ROOT / "scripts" / "generate_methods_figures.py")
generate_methods_figures = importlib.util.module_from_spec(SPEC_FIGURES)
SPEC_FIGURES.loader.exec_module(generate_methods_figures)


def ensure_required_method_figures_exist():
    """Create required figure artifacts from committed CSVs for clean CI checkouts."""
    generate_methods_figures.generate_figures(ROOT / "results", ROOT / "reports", FIGURE_PREFIX, "roc_auc")


def test_cli_help_smoke_for_all_scripts():
    for name in SCRIPT_NAMES:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--help"], cwd=ROOT, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, name + " failed: " + result.stderr
        assert "usage" in result.stdout.lower()


def test_run_benchmark_dry_run_smoke():
    result = subprocess.run([sys.executable, "scripts/run_benchmark.py", "--config", "configs/benchmark.yaml", "--dry-run"], cwd=ROOT, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0
    assert "dataset" in result.stdout.lower() or "config" in result.stdout.lower()


def test_release_archive_audit_passes_after_generating_required_outputs():
    ensure_required_method_figures_exist()
    audit = build_release_archive.audit_release(ROOT)
    assert audit["passed"]
    assert audit["missing_required_files"] == []
    assert audit["disallowed_filenames"] == []
    assert audit["raw_data_like_directories"] == []


def test_release_archive_builder_excludes_cache_files(tmp_path):
    ensure_required_method_figures_exist()
    output = tmp_path / "release.zip"
    result = build_release_archive.build_archive(ROOT, output, top_level_name="release-test")
    assert result["passed"]
    assert result["archive_file_count"] == result["n_included_files"]
    assert result["archive_junk_entries"] == []
    assert output.exists() and output.stat().st_size > 0
