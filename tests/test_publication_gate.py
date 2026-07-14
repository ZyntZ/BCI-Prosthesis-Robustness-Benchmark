import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_release_manifest", ROOT / "scripts" / "build_release_manifest.py")
build_release_manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_release_manifest)


def test_release_manifest_builder_hashes_required_files():
    manifest = build_release_manifest.build_manifest(
        ROOT,
        ROOT / "results",
        ROOT / "reports",
        ["PhysionetMI_dev10"],
    )
    paths = {row["path"] for row in manifest["file_hashes_sha256"]}
    assert "pyproject.toml" in paths
    assert "scripts/validate_results.py" in paths
    assert "scripts/build_release_manifest.py" in paths
    assert isinstance(manifest["package_versions"], dict)


def test_release_manifest_detects_expected_outputs_without_mutating_inputs(tmp_path):
    manifest = build_release_manifest.build_manifest(
        ROOT,
        tmp_path,
        tmp_path,
        ["missing_prefix"],
    )
    assert not manifest["release_ready"]
    assert manifest["missing_expected_outputs"]
