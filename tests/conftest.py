"""Test configuration: load the cleanmyos script as an importable module."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "cleanmyos"

if "cleanmyos_mod" not in sys.modules:
    spec = importlib.util.spec_from_file_location("cleanmyos_mod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cleanmyos_mod"] = mod
    spec.loader.exec_module(mod)

cleanmyos_mod = sys.modules["cleanmyos_mod"]
