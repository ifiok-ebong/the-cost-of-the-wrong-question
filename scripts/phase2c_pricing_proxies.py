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
    subs = pd.read_csv(RAW / "ravenstack_subscriptions.csv")
    subs["start_date"] = pd.to_datetime(subs["start_date"], errors="coerce")
    subs["end_date"] = pd.to_datetime(subs["end_date"], errors="coerce")

    # Load account-month MRR
    am = pd.read_csv(PROC / "account_month_mrr.csv")
    am["month"] = pd.to_datetime(am["month"], errors="coerce")

    # ARPA drift is already in monthly_net_revenue, but compute explicitly here for isolation
    monthly = pd.read_csv(PROC / "monthly_net_revenue.csv")
    monthly["month"] = pd.to_datetime(monthly["month"], errors="coerce")
    arpa = monthly[["month", "arpa", "active_accounts", "net_revenue"]].copy()

    # Plan tier mix by month using subscription-month expansion
    s = subs.dropna(subset=["account_id", "start_date", "end_date", "plan_tier"]).copy()
    s["start_month"] = month_floor(s["start_date"])
    s["end_month"] = month_floor(s["end_date"])

    rows = []
    for r in s.itertuples(index=False):
        m = r.start_month
        while m <= r.end_month:
            rows.append({
                "account_id": r.account_id,
                "month": m,
                "plan_tier": r.plan_tier,
                "seats": r.seats,
                "mrr_amount": r.mrr_amount,
            })
            m = (pd.Timestamp(m) + pd.offsets.MonthBegin(1)).normalize()

    sm = pd.DataFrame(rows)
    # Aggregate plan tier mix by account-month (take highest MRR subscription tier for simplicity)
    if not sm.empty:
        # rank within account-month by mrr_amount
        sm = sm.sort_values(["account_id", "month", "mrr_amount"], ascending=[True, True, False])
        sm_top = sm.groupby(["account_id", "month"], as_index=False).first()

        tier_mix = (
            sm_top.groupby(["month", "plan_tier"], as_index=False)
            .agg(accounts=("account_id", "nunique"), seats=("seats", "sum"), mrr=("mrr_amount", "sum"))
            .sort_values(["month", "accounts"], ascending=[True, False])
        )

        # Share by month
        totals = tier_mix.groupby("month", as_index=False).agg(total_accounts=("accounts", "sum"), total_mrr=("mrr", "sum"))
        tier_mix = tier_mix.merge(totals, on="month", how="left")
        tier_mix["account_share"] = tier_mix["accounts"] / tier_mix["total_accounts"]
        tier_mix["mrr_share"] = tier_mix["mrr"] / tier_mix["total_mrr"]
    else:
        tier_mix = pd.DataFrame(columns=["month", "plan_tier", "accounts", "seats", "mrr", "total_accounts", "total_mrr", "account_share", "mrr_share"])

    # Seat migration proxy: average seats per active account per month (from subscriptions top-tier view)
    if not sm.empty:
        seats_monthly = (
            sm_top.groupby("month", as_index=False)
            .agg(avg_seats=("seats", "mean"), median_seats=("seats", "median"))
            .sort_values("month")
        )
    else:
        seats_monthly = pd.DataFrame(columns=["month", "avg_seats", "median_seats"])

    # Save outputs
    arpa.to_csv(PROC / "hypC_arpa_drift.csv", index=False)
    tier_mix.to_csv(PROC / "hypC_plan_tier_mix.csv", index=False)
    seats_monthly.to_csv(PROC / "hypC_seat_migration.csv", index=False)

    print("ARPA months:", arpa["month"].min(), "to", arpa["month"].max())
    print("Plan tiers:", sorted(set(tier_mix["plan_tier"].dropna().unique().tolist())))


if __name__ == "__main__":
    main()
