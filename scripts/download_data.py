"""Download dataset(s) for this project and write SHA256 hashes.

Dataset:
- rivalytics/saas-subscription-and-churn-analytics-dataset (MIT)

Policy:
- Raw data is not committed by default.
- Requires Kaggle CLI configured via ~/.kaggle/kaggle.json

Usage:
- python scripts/download_data.py
"""

from __future__ import annotations

import hashlib
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "ravenstack"
HASHES_FILE = ROOT / "data" / "hashes.sha256"

DATASET_REF = "rivalytics/saas-subscription-and-churn-analytics-dataset"
EXPECTED_FILES = [
    "ravenstack_accounts.csv",
    "ravenstack_subscriptions.csv",
    "ravenstack_churn_events.csv",
    "ravenstack_feature_usage.csv",
    "ravenstack_support_tickets.csv",
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_hashes(files: list[pathlib.Path]) -> None:
    lines = [f"{sha256_file(p)}  {p.relative_to(ROOT)}" for p in files]
    HASHES_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def have_expected_files() -> bool:
    return all((RAW_DIR / f).exists() for f in EXPECTED_FILES)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not have_expected_files():
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

    files = sorted([p for p in RAW_DIR.glob("*.csv") if p.is_file()])
    write_hashes(files)

    print(f"Dataset ready in: {RAW_DIR}")
    print(f"Hashes written to: {HASHES_FILE}")


if __name__ == "__main__":
    main()
