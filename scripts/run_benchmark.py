from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import yaml

from moabb.paradigms import LeftRightImagery
from moabb.utils import set_download_dir

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bci_robustness.core import evaluate_subject_with_dropout, subject_bootstrap_ci


DATASET_REGISTRY = {
    "PhysionetMI": PhysionetMI,
    "PhysionetMotorImagery": PhysionetMI,
    "BNCI2014-001": BNCI2014_001,
}


#Забыл. Переделать.