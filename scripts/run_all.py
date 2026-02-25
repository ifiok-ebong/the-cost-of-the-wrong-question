"""Run the full analysis pipeline end-to-end.

This is a convenience entrypoint for reviewers.

Default mode runs in the current working tree.
Safe-test mode (--safe-test) runs the pipeline inside a temporary copy of the repo,
optionally seeding it with any existing local raw data, so it can't overwrite
your committed artifacts.

Prereqs:
- Python 3.11+ (tested on 3.12)
- Dependencies installed: pip install -r requirements.txt
- Kaggle configured: ~/.kaggle/kaggle.json (only needed if raw data is absent)

Usage:
- python scripts/run_all.py
- python scripts/run_all.py --safe-test

Outputs:
- data/processed/*.csv
- analysis_recommendation.md
- docs/figures/*.png
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path) -> None:
    print("\n$", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd))


def run_pipeline(cwd: Path) -> None:
    # Data (idempotent; if raw data exists it will just write hashes)
    run([sys.executable, "scripts/download_data.py"], cwd)

    # Phase 1
    run([sys.executable, "scripts/phase1_baseline.py"], cwd)

    # Phase 2 hypotheses
    run([sys.executable, "scripts/phase2a_acquisition_output.py"], cwd)
    run([sys.executable, "scripts/phase2b_ltv_deterioration.py"], cwd)
    run([sys.executable, "scripts/phase2c_pricing_proxies.py"], cwd)

    # Phase 3 comparison
    run([sys.executable, "scripts/phase3_compare_drivers.py"], cwd)

    # Phase 4 recommendation
    run([sys.executable, "scripts/phase4_recommendation.py"], cwd)


def safe_test() -> int:
    """Run the pipeline inside a temp copy of the repo.

    This avoids overwriting any local outputs in your current working tree.
    It also reduces Kaggle dependence by copying any existing local raw data
    into the temp copy when available.
    """
    with tempfile.TemporaryDirectory(prefix="runall_safe_test_") as td:
        troot = Path(td)

        # Export a clean copy of the repo at HEAD (no .git dir)
        archive_cmd = ["git", "archive", "--format=tar", "HEAD"]
        tar_path = troot / "repo.tar"
        with tar_path.open("wb") as f:
            subprocess.check_call(archive_cmd, cwd=str(ROOT), stdout=f)
        run(["tar", "-xf", str(tar_path), "-C", str(troot)], troot)
        tar_path.unlink(missing_ok=True)

        # Seed raw data if present locally
        src_raw = ROOT / "data" / "raw" / "ravenstack"
        dst_raw = troot / "data" / "raw" / "ravenstack"
        if src_raw.exists():
            dst_raw.mkdir(parents=True, exist_ok=True)
            for p in src_raw.glob("*.csv"):
                shutil.copy2(p, dst_raw / p.name)

        # Create venv + install requirements inside temp
        run([sys.executable, "-m", "venv", ".venv"], troot)
        pip = troot / ".venv" / "bin" / "pip"
        py = troot / ".venv" / "bin" / "python"
        run([str(pip), "install", "-r", "requirements.txt"], troot)

        # Execute pipeline using temp venv python
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        def run_env(cmd: list[str]) -> None:
            print("\n$", " ".join(cmd))
            subprocess.check_call(cmd, cwd=str(troot), env=env)

        # Data + phases
        # In safe-test mode, avoid surprising failures due to Kaggle CLI setup.
        # If raw CSVs are present (seeded from the current working tree), skip the Kaggle download call.
        raw_dir = troot / "data" / "raw" / "ravenstack"
        expected = [
            "ravenstack_accounts.csv",
            "ravenstack_subscriptions.csv",
            "ravenstack_churn_events.csv",
            "ravenstack_feature_usage.csv",
            "ravenstack_support_tickets.csv",
        ]
        have_raw = raw_dir.exists() and all((raw_dir / f).exists() for f in expected)
        if have_raw:
            print('\nRaw data present in temp copy; skipping Kaggle download step.')
        else:
            # Attempt download only if Kaggle CLI is available; otherwise fail with a clear message.
            kaggle_ok = shutil.which('kaggle') is not None
            if not kaggle_ok:
                raise RuntimeError(
                    'Safe-test requires either (a) existing raw CSVs in data/raw/ravenstack/ '
                    'or (b) Kaggle CLI configured. Kaggle CLI not found.'
                )
            run_env([str(py), 'scripts/download_data.py'])

        run_env([str(py), "scripts/phase1_baseline.py"])
        run_env([str(py), "scripts/phase2a_acquisition_output.py"])
        run_env([str(py), "scripts/phase2b_ltv_deterioration.py"])
        run_env([str(py), "scripts/phase2c_pricing_proxies.py"])
        run_env([str(py), "scripts/phase3_compare_drivers.py"])
        run_env([str(py), "scripts/phase4_recommendation.py"])

        # Quick success signal
        must_exist = [
            troot / "analysis_recommendation.md",
            troot / "data" / "processed" / "monthly_net_revenue.csv",
            troot / "data" / "processed" / "phase3_driver_comparison.csv",
        ]
        missing = [str(p) for p in must_exist if not p.exists()]
        if missing:
            raise RuntimeError("Safe-test completed but expected outputs missing: " + ", ".join(missing))

        print("\nSAFE-TEST OK (ran in temp copy):", troot)

    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--safe-test",
        action="store_true",
        help="Run inside a temporary repo copy so existing local outputs are not overwritten.",
    )
    args = ap.parse_args()

    if args.safe_test:
        return safe_test()

    run_pipeline(ROOT)

    print("\nDone.")
    print("Key outputs:")
    print("- analysis_recommendation.md")
    print("- data/processed/")
    print("- docs/figures/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
