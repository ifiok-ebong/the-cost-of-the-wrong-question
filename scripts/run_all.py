"""Run the full analysis pipeline end-to-end.

This is a convenience entrypoint for reviewers.

Prereqs:
- Python 3.11+ (tested on 3.12)
- Dependencies installed: pip install -r requirements.txt
- Kaggle configured: ~/.kaggle/kaggle.json

Usage:
- python scripts/run_all.py

Outputs:
- data/processed/*.csv
- analysis_recommendation.md
- docs/figures/*.png
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("\n$", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(ROOT))


def main() -> int:
    # Data
    run([sys.executable, "scripts/download_data.py"])

    # Phase 1
    run([sys.executable, "scripts/phase1_baseline.py"])

    # Phase 2 hypotheses
    run([sys.executable, "scripts/phase2a_acquisition_output.py"])
    run([sys.executable, "scripts/phase2b_ltv_deterioration.py"])
    run([sys.executable, "scripts/phase2c_pricing_proxies.py"])

    # Phase 3 comparison
    run([sys.executable, "scripts/phase3_compare_drivers.py"])

    # Phase 4 recommendation
    run([sys.executable, "scripts/phase4_recommendation.py"])

    print("\nDone.")
    print("Key outputs:")
    print("- analysis_recommendation.md")
    print("- data/processed/")
    print("- docs/figures/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
