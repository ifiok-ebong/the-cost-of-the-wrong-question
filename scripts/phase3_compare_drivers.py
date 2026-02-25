from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # Load processed artifacts
    monthly = pd.read_csv(PROC / "monthly_net_revenue.csv", parse_dates=["month"])

    # Hyp A
    new_accounts = pd.read_csv(PROC / "hypA_new_accounts_per_month.csv", parse_dates=["month"])
    starting = pd.read_csv(PROC / "hypA_starting_mrr_trend.csv", parse_dates=["month"])

    # Hyp B
    bridge = pd.read_csv(PROC / "hypB_revenue_bridge_components.csv", parse_dates=["month"])

    # Merge base timeline
    df = (
        monthly.merge(new_accounts, on="month", how="left")
        .merge(starting, on="month", how="left")
        .merge(bridge, on="month", how="left")
        .sort_values("month")
    )

    # --- Signed contributions (heuristics) ---
    # Acquisition contribution proxy: delta new accounts * avg starting mrr
    df["new_accounts"] = df["new_accounts"].fillna(0)
    df["avg_starting_mrr"] = df["avg_starting_mrr"].fillna(0)
    df["acq_contribution"] = df["new_accounts"].diff() * df["avg_starting_mrr"]

    # Retention contribution: churned + contraction - expansion
    for c in ["churned_mrr", "contraction_mrr", "expansion_mrr"]:
        if c in df.columns:
            df[c] = df[c].fillna(0)
    # Positive retention_contribution means drag under this convention.
    df["retention_contribution"] = df["churned_mrr"] + df["contraction_mrr"] - df["expansion_mrr"]

    # Pricing contribution proxy: ARPA drift (delta ARPA * active accounts)
    # Positive pricing_contribution means tailwind (ARPA expansion); negative implies compression/headwind.
    df["arpa"] = df["arpa"].fillna(0)
    df["pricing_contribution"] = df["arpa"].diff() * df["active_accounts"]

    # --- View 1: Largest lever (magnitude) ---
    # Identifies the biggest moving component (largest lever) over the window; direction is handled separately.
    df["acq_abs"] = df["acq_contribution"].abs()
    df["ret_abs"] = df["retention_contribution"].abs()
    df["prc_abs"] = df["pricing_contribution"].abs()

    for col in ["acq_abs", "ret_abs", "prc_abs"]:
        df[col + "_3m"] = df[col].rolling(3).sum()

    def leader_lever(row):
        vals = {
            "acquisition": row.get("acq_abs_3m"),
            "retention": row.get("ret_abs_3m"),
            "pricing": row.get("prc_abs_3m"),
        }
        vals = {k: float(v) for k, v in vals.items() if pd.notna(v)}
        if not vals:
            return None
        return max(vals, key=vals.get)

    df["leader_lever_3m"] = df.apply(leader_lever, axis=1)

    # --- View 2: Largest pressure (directional drag) ---
    # Only count headwinds/drag when comparing "pressure".
    df["acq_pressure"] = (-df["acq_contribution"]).clip(lower=0)  # acquisition headwind only
    df["ret_pressure"] = df["retention_contribution"].clip(lower=0)  # churn+contraction drag
    df["prc_pressure"] = (-df["pricing_contribution"]).clip(lower=0)  # pricing compression only

    for col in ["acq_pressure", "ret_pressure", "prc_pressure"]:
        df[col + "_3m"] = df[col].rolling(3).sum()

    def leader_pressure(row):
        vals = {
            "acquisition": row.get("acq_pressure_3m"),
            "retention": row.get("ret_pressure_3m"),
            "pricing": row.get("prc_pressure_3m"),
        }
        vals = {k: float(v) for k, v in vals.items() if pd.notna(v)}
        if not vals:
            return None
        return max(vals, key=vals.get)

    df["leader_pressure_3m"] = df.apply(leader_pressure, axis=1)

    # Persist
    out_cols = [
        "month",
        "net_revenue",
        "mom_growth",
        "yoy_growth",
        "new_accounts",
        "avg_starting_mrr",
        "acq_contribution",
        "retention_contribution",
        "pricing_contribution",
        # lever
        "acq_abs_3m",
        "ret_abs_3m",
        "prc_abs_3m",
        "leader_lever_3m",
        # pressure
        "acq_pressure_3m",
        "ret_pressure_3m",
        "prc_pressure_3m",
        "leader_pressure_3m",
    ]
    out = df[out_cols].copy()
    out.to_csv(PROC / "phase3_driver_comparison.csv", index=False)

    print(out.tail(6).to_string(index=False))


if __name__ == "__main__":
    main()
