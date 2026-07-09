"""Pytest path configuration for the modular AccessAtlas package."""

from pathlib import Path
import sys


MODULAR_ROOT = Path(__file__).resolve().parents[1] / "modular"
if str(MODULAR_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULAR_ROOT))
