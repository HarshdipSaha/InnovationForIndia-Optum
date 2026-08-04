#!/usr/bin/env python3
"""SAAKSHI demo entry point.

    python run_demo.py

Zero dependencies beyond the Python standard library. No network access.
Exit code 0 iff every detector re-derived its target CAG finding.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from saakshi.demo.report import run  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(run())
