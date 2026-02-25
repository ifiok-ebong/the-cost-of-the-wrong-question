"""Lightweight verification checks for reviewers.

This is not a full test suite. It validates that expected outputs exist and
contain the minimum required columns/structure.

Usage:
  python scripts/verify_outputs.py

Typical flow:
  python scripts/run_all.py --safe-test
  python scripts/verify_outputs.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"


def must_exist(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing expected file: {path}")
    if path.is_file() and path.stat().st_size == 0:
        raise SystemExit(f"Expected non-empty file: {path}")


def main() -> None:
    must_exist(ROOT / "analysis_recommendation.md")
    must_exist(ROOT / "data" / "hashes.sha256")

    expected_processed = [
        "monthly_net_revenue.csv",
        "account_month_mrr.csv",
        "hypA_new_accounts_per_month.csv",
        "hypA_referral_source_mix.csv",
        "hypA_starting_mrr_trend.csv",
        "hypB_churn_rate_overall.csv",
        "hypB_churn_by_tenure_bucket.csv",
        "hypB_revenue_bridge_components.csv",
        "hypC_arpa_drift.csv",
        "hypC_plan_tier_mix.csv",
        "hypC_seat_migration.csv",
        "phase3_driver_comparison.csv",
    ]

    for f in expected_processed:
        must_exist(PROC / f)

    comp = pd.read_csv(PROC / "phase3_driver_comparison.csv")
    required_cols = {
        "month",
        "leader_lever_3m",
        "leader_pressure_3m",
        "acq_pressure_3m",
        "ret_pressure_3m",
        "prc_pressure_3m",
    }
    missing = required_cols - set(comp.columns)
    if missing:
        raise SystemExit(f"phase3_driver_comparison.csv missing columns: {sorted(missing)}")

    if comp["month"].isna().any():
        raise SystemExit("phase3_driver_comparison.csv has null month values")

    print("OK: outputs present and minimally valid")


if __name__ == "__main__":
    main()
