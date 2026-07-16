#!/usr/bin/env python3
"""Start Demo 5 on localhost using the active Python environment."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "triangle_workshop.py"


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP),
        "--server.address=localhost",
        "--server.maxUploadSize=200",
    ]
    print("Iniciando Demo 5 en modo local...")
    print("Los archivos seleccionados no se envían a GitHub.")
    try:
        exit_code = subprocess.call(command, cwd=ROOT)
        return 0 if exit_code < 0 else exit_code
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
