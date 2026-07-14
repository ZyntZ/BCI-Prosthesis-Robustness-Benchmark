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

SPEC = importlib.util.spec_from_file_location("build_release_archive", ROOT / "scripts" / "build_release_archive.py")
build_release_archive = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_release_archive)


def test_cli_help_smoke_for_all_scripts():
    for name in SCRIPT_NAMES:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--help"], cwd=ROOT, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, name + " failed: " + result.stderr
        assert "usage" in result.stdout.lower()


def test_run_benchmark_dry_run_smoke():
    result = subprocess.run([sys.executable, "scripts/run_benchmark.py", "--config", "configs/benchmark.yaml", "--dry-run"], cwd=ROOT, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0
    assert "dataset" in result.stdout.lower() or "config" in result.stdout.lower()


def test_release_archive_audit_passes_after_generated_outputs_exist():
    audit = build_release_archive.audit_release(ROOT)
    assert audit["passed"]
    assert audit["missing_required_files"] == []
    assert audit["disallowed_filenames"] == []
    assert audit["raw_data_like_directories"] == []


def test_release_archive_builder_excludes_cache_files(tmp_path):
    output = tmp_path / "release.zip"
    result = build_release_archive.build_archive(ROOT, output, top_level_name="release-test")
    assert result["passed"]
    assert result["archive_file_count"] == result["n_included_files"]
    assert result["archive_junk_entries"] == []
    assert output.exists() and output.stat().st_size > 0
