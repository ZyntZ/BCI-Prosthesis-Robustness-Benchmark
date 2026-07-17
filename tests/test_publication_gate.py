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


def test_manifest_excludes_local_environments_and_raw_data(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "kept.py").write_text("print('kept')\n", encoding="utf-8")
    for directory in [".venv", "moabb_data", "dist"]:
        path = root / directory
        path.mkdir()
        (path / "excluded.py").write_text("print('excluded')\n", encoding="utf-8")
    paths = {path.relative_to(root).as_posix() for path in build_release_manifest.iter_manifest_files(root)}
    assert "kept.py" in paths
    assert not any("excluded.py" in path for path in paths)


def test_default_release_scope_includes_full_physionet_and_uses_its_figures():
    full = "PhysionetMI_PhysionetMI_all_riemann_lr"
    assert full in build_release_manifest.DEFAULT_PREFIXES
    assert build_release_manifest.METHODS_FIGURE_PREFIXES == [full]
