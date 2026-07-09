"""Pytest configuration for the modular AccessAtlas package."""

from pathlib import Path
import sys
import types


MODULAR_ROOT = Path(__file__).resolve().parents[1] / "modular"
if str(MODULAR_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULAR_ROOT))


# Several core modules use Streamlit session state as the reference runtime
# adapter. Pure unit tests should remain runnable without installing Streamlit.
try:
    import streamlit  # noqa: F401
except ModuleNotFoundError:
    streamlit_stub = types.ModuleType("streamlit")
    streamlit_stub.session_state = {}
    sys.modules["streamlit"] = streamlit_stub
