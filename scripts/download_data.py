"""Download dataset(s) for this project and write SHA256 hashes.

Dataset:
- rivalytics/saas-subscription-and-churn-analytics-dataset (MIT)

Notes:
- Requires Kaggle CLI configured via ~/.kaggle/kaggle.json
- This script writes data into data/raw/ravenstack
"""

from __future__ import annotations

import hashlib
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "ravenstack"
HASHES_FILE = ROOT / "data" / "hashes.sha256"

DATASET_REF = "rivalytics/saas-subscription-and-churn-analytics-dataset"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Download and unzip into RAW_DIR
    subprocess.check_call(
        [
            "kaggle",
            "datasets",
            "download",
            "-d",
            DATASET_REF,
            "-p",
            str(RAW_DIR),
            "--unzip",
        ]
    )

    # Write hashes
    files = sorted([p for p in RAW_DIR.glob("*.csv") if p.is_file()])
    lines = []
    for p in files:
        lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT)}")

    HASHES_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Downloaded {len(files)} CSV files to {RAW_DIR}")
    print(f"Wrote hashes to {HASHES_FILE}")


if __name__ == "__main__":
    main()
