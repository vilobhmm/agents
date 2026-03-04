"""Pytest configuration — ensures the project root is on sys.path."""

import sys
from pathlib import Path

# Add project root to path so 'harness' and 'agents' are importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
