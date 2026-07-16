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
