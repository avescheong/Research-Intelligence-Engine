#!/usr/bin/env python3
"""
RIE Portable OS Root Entrypoint
Forwarding launcher to engine/cli.py.
"""
import sys
from pathlib import Path

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.cli import main

if __name__ == "__main__":
    main()
