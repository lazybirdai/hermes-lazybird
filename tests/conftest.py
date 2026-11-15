"""Path shim so tests can import the plugin module by name."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lazybird"))
