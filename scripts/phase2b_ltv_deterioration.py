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
    accounts = pd.read_csv(RAW / "ravenstack_accounts.csv")
    subs = pd.read_csv(RAW / "ravenstack_subscriptions.csv")
    churn_events = pd.read_csv(RAW / "ravenstack_churn_events.csv")

    accounts["signup_date"] = pd.to_datetime(accounts["signup_date"], errors="coerce")
    subs["start_date"] = pd.to_datetime(subs["start_date"], errors="coerce")
    subs["end_date"] = pd.to_datetime(subs["end_date"], errors="coerce")
    churn_events["churn_date"] = pd.to_datetime(churn_events["churn_date"], errors="coerce")

    # Load account-month MRR built in Phase 1
    am = pd.read_csv(PROC / "account_month_mrr.csv")
    am["month"] = pd.to_datetime(am["month"], errors="coerce")

    # Add tenure months proxy based on signup_date
    a = accounts.dropna(subset=["account_id", "signup_date"]).copy()
    a["signup_month"] = month_floor(a["signup_date"])

    am = am.merge(a[["account_id", "signup_month"]], on="account_id", how="left")
    am["tenure_months"] = ((am["month"].dt.to_period("M") - am["signup_month"].dt.to_period("M")).apply(lambda x: x.n)).astype("Int64")

    # Tenure buckets
    def bucket(t):
        if pd.isna(t) or t < 0:
            return "unknown"
        if t <= 2:
            return "0-2"
        if t <= 5:
            return "3-5"
        if t <= 11:
            return "6-11"
        return "12+"

    am["tenure_bucket"] = am["tenure_months"].apply(bucket)

    # Churn month at account level (from churn_events)
    ce = churn_events.dropna(subset=["account_id", "churn_date"]).copy()
    ce["churn_month"] = month_floor(ce["churn_date"])

    # If multiple churn events exist, take earliest churn_month
    churn_month = ce.sort_values(["account_id", "churn_month"]).groupby("account_id", as_index=False).first()[["account_id", "churn_month"]]

    # Add prior-month MRR for churn impact timing (t-1)
    am = am.sort_values(["account_id", "month"])
    am["prior_mrr"] = am.groupby("account_id")["mrr_amount"].shift(1)

    # Monthly churned revenue: for accounts whose churn_month == month, take prior_mrr
    am = am.merge(churn_month, on="account_id", how="left")
    am["is_churn_month"] = am["churn_month"].eq(am["month"])
    churn_rev = (
        am.loc[am["is_churn_month"].fillna(False)]
        .groupby("month", as_index=False)
        .agg(churned_mrr=("prior_mrr", "sum"), churned_accounts=("account_id", "nunique"))
        .sort_values("month")
    )

    # Churn rate (logo churn) by month overall and by tenure bucket
    churn_logo_overall = churn_rev[["month", "churned_accounts"]].copy()

    # Denominator: active accounts in prior month
    active = am.groupby("month", as_index=False).agg(active_accounts=("account_id", "nunique"), start_mrr=("mrr_amount", "sum"))
    active["prior_active_accounts"] = active["active_accounts"].shift(1)
    active["prior_start_mrr"] = active["start_mrr"].shift(1)

    churn_logo_overall = churn_logo_overall.merge(active[["month", "prior_active_accounts"]], on="month", how="left")
    churn_logo_overall["churn_rate"] = churn_logo_overall["churned_accounts"] / churn_logo_overall["prior_active_accounts"]

    # Tenure-segmented churn (approx): compute churned accounts by tenure bucket at churn month
    churn_tenure = (
        am.loc[am["is_churn_month"].fillna(False)]
        .groupby(["month", "tenure_bucket"], as_index=False)
        .agg(churned_accounts=("account_id", "nunique"), churned_mrr=("prior_mrr", "sum"))
        .sort_values(["month", "tenure_bucket"])
    )

    # Expansion / contraction from account-month MRR deltas (ignore churn months for delta classification)
    am["delta_mrr"] = am["mrr_amount"] - am["prior_mrr"]
    am["expansion_mrr"] = am["delta_mrr"].where(am["delta_mrr"] > 0, 0)
    am["contraction_mrr"] = (-am["delta_mrr"]).where(am["delta_mrr"] < 0, 0)

    bridge = (
        am.groupby("month", as_index=False)
        .agg(
            expansion_mrr=("expansion_mrr", "sum"),
            contraction_mrr=("contraction_mrr", "sum"),
        )
        .sort_values("month")
        .merge(churn_rev[["month", "churned_mrr"]], on="month", how="left")
        .merge(active[["month", "prior_start_mrr"]], on="month", how="left")
    )
    bridge["churned_mrr"] = bridge["churned_mrr"].fillna(0)

    # NRR-style signal (using prior month start MRR)
    bridge["net_retained_mrr"] = bridge["prior_start_mrr"] + bridge["expansion_mrr"] - bridge["contraction_mrr"] - bridge["churned_mrr"]
    bridge["nrr"] = bridge["net_retained_mrr"] / bridge["prior_start_mrr"]

    # Save outputs
    churn_logo_overall.to_csv(PROC / "hypB_churn_rate_overall.csv", index=False)
    churn_tenure.to_csv(PROC / "hypB_churn_by_tenure_bucket.csv", index=False)
    bridge.to_csv(PROC / "hypB_revenue_bridge_components.csv", index=False)

    # Print tight summary
    print("Bridge months:", bridge["month"].min(), "to", bridge["month"].max())
    print("NRR latest:", float(bridge.dropna(subset=["nrr"]).iloc[-1]["nrr"]))


if __name__ == "__main__":
    main()
