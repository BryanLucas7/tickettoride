"""Ensure backend package is importable during pytest runs."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
BACKEND_STR = str(BACKEND_ROOT)
if BACKEND_STR not in sys.path:
    sys.path.insert(0, BACKEND_STR)
