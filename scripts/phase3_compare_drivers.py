from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ravenstack"
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)


def month_floor(s: pd.Series) -> pd.Series:
    return s.dt.to_period("M").dt.to_timestamp()


def main() -> None:
    # Load processed artifacts
    monthly = pd.read_csv(PROC / "monthly_net_revenue.csv", parse_dates=["month"])
    account_month = pd.read_csv(PROC / "account_month_mrr.csv", parse_dates=["month"])

    # Hyp A
    new_accounts = pd.read_csv(PROC / "hypA_new_accounts_per_month.csv", parse_dates=["month"])
    starting = pd.read_csv(PROC / "hypA_starting_mrr_trend.csv", parse_dates=["month"])

    # Hyp B
    bridge = pd.read_csv(PROC / "hypB_revenue_bridge_components.csv", parse_dates=["month"])

    # Merge base timeline
    df = monthly.merge(new_accounts, on="month", how="left").merge(starting, on="month", how="left").merge(bridge, on="month", how="left")

    # Acquisition contribution proxy: delta new accounts * avg starting mrr
    df["new_accounts"] = df["new_accounts"].fillna(0)
    df["avg_starting_mrr"] = df["avg_starting_mrr"].fillna(0)
    df["acq_contribution"] = df["new_accounts"].diff() * df["avg_starting_mrr"]

    # Retention contribution: churned + contraction - expansion
    for c in ["churned_mrr", "contraction_mrr", "expansion_mrr"]:
        if c in df.columns:
            df[c] = df[c].fillna(0)
    df["retention_contribution"] = df["churned_mrr"] + df["contraction_mrr"] - df["expansion_mrr"]

    # Pricing contribution proxy: ARPA drift (delta ARPA * active accounts)
    # Interpret negative ARPA delta as pricing compression signal.
    df["arpa"] = df["arpa"].fillna(0)
    df["pricing_contribution"] = df["arpa"].diff() * df["active_accounts"]

    # Normalize to absolute impact magnitude for comparison
    # This identifies the largest moving component (largest lever) over the window; direction is handled separately in interpretation.
    df["acq_abs"] = df["acq_contribution"].abs()
    df["ret_abs"] = df["retention_contribution"].abs()
    df["prc_abs"] = df["pricing_contribution"].abs()

    # Rolling 3-month sums for dominance stability
    for col in ["acq_abs", "ret_abs", "prc_abs"]:
        df[col + "_3m"] = df[col].rolling(3).sum()

    # Determine leader each month based on 3-month impact
    def leader(row):
        vals = {"acquisition": row.get("acq_abs_3m"), "ltv": row.get("ret_abs_3m"), "pricing": row.get("prc_abs_3m")}
        vals = {k: float(v) for k, v in vals.items() if pd.notna(v)}
        if not vals:
            return None
        return max(vals, key=vals.get)

    df["leader_3m"] = df.apply(leader, axis=1)

    # Persist
    out = df[[
        "month",
        "net_revenue",
        "mom_growth",
        "yoy_growth",
        "new_accounts",
        "avg_starting_mrr",
        "acq_contribution",
        "retention_contribution",
        "pricing_contribution",
        "acq_abs_3m",
        "ret_abs_3m",
        "prc_abs_3m",
        "leader_3m",
    ]].copy()

    out.to_csv(PROC / "phase3_driver_comparison.csv", index=False)

    # Print last 6 rows for quick review
    print(out.tail(6).to_string(index=False))


if __name__ == "__main__":
    main()
