"""Download dataset(s) for this project.

Policy:
- Do not commit raw data unless explicitly CC0.
- Record hashes in data/hashes.sha256.

Fill in once dataset is selected.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    raise SystemExit(
        "Dataset not selected yet. Once selected, this script will download the files and write hashes."
    )


if __name__ == "__main__":
    main()
