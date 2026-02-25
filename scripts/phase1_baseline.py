from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ravenstack"
OUT_DIR = ROOT / "data" / "processed"


@dataclass
class BaselineResult:
    monthly_net_revenue: pd.DataFrame


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    accounts = pd.read_csv(RAW / "ravenstack_accounts.csv")
    subs = pd.read_csv(RAW / "ravenstack_subscriptions.csv")
    churn = pd.read_csv(RAW / "ravenstack_churn_events.csv")

    accounts["signup_date"] = pd.to_datetime(accounts["signup_date"], errors="coerce")
    subs["start_date"] = pd.to_datetime(subs["start_date"], errors="coerce")
    subs["end_date"] = pd.to_datetime(subs["end_date"], errors="coerce")
    churn["churn_date"] = pd.to_datetime(churn["churn_date"], errors="coerce")

    return accounts, subs, churn


def month_floor(s: pd.Series) -> pd.Series:
    return s.dt.to_period("M").dt.to_timestamp()


def build_account_month_mrr(subs: pd.DataFrame) -> pd.DataFrame:
    # Interpret each subscription row as active over [start_date, end_date] with constant mrr_amount.
    # Expand to account-month records.
    s = subs.dropna(subset=["account_id", "start_date", "end_date", "mrr_amount"]).copy()

    s["start_month"] = month_floor(s["start_date"])
    s["end_month"] = month_floor(s["end_date"])

    rows = []
    for r in s.itertuples(index=False):
        m = r.start_month
        # include end_month as active month if end_date is within that month.
        while m <= r.end_month:
            rows.append(
                {
                    "account_id": r.account_id,
                    "month": m,
                    "subscription_id": r.subscription_id,
                    "plan_tier": r.plan_tier,
                    "seats": r.seats,
                    "mrr_amount": float(r.mrr_amount),
                    "upgrade_flag": bool(r.upgrade_flag),
                    "downgrade_flag": bool(r.downgrade_flag),
                    "churn_flag": bool(r.churn_flag),
                }
            )
            m = (pd.Timestamp(m) + pd.offsets.MonthBegin(1)).normalize()

    am = pd.DataFrame(rows)
    if am.empty:
        return am

    # Aggregate to account-month MRR (sum across concurrent subs if any)
    am_agg = (
        am.groupby(["account_id", "month"], as_index=False)
        .agg(
            mrr_amount=("mrr_amount", "sum"),
            any_upgrade=("upgrade_flag", "max"),
            any_downgrade=("downgrade_flag", "max"),
            any_churn=("churn_flag", "max"),
        )
        .sort_values(["month", "account_id"])
    )
    return am_agg


def compute_monthly_net_revenue(am: pd.DataFrame) -> pd.DataFrame:
    # Net Revenue (Monthly) = sum of account-month MRR
    m = (
        am.groupby("month", as_index=False)
        .agg(net_revenue=("mrr_amount", "sum"),
             active_accounts=("account_id", "nunique"),
             arpa=("mrr_amount", "mean"))
        .sort_values("month")
    )

    m["mom_growth"] = m["net_revenue"].pct_change()
    m["yoy_growth"] = m["net_revenue"].pct_change(12)
    return m


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    accounts, subs, churn = load_raw()

    am = build_account_month_mrr(subs)
    if am.empty:
        raise SystemExit("No account-month rows built from subscriptions")

    monthly = compute_monthly_net_revenue(am)

    # Persist
    am.to_csv(OUT_DIR / "account_month_mrr.csv", index=False)
    monthly.to_csv(OUT_DIR / "monthly_net_revenue.csv", index=False)

    # Print a tight summary for logs
    print("Built account-month table:", am.shape)
    print("Monthly net revenue series:", monthly.shape)
    print("Month range:", monthly["month"].min(), "to", monthly["month"].max())
    print("Latest month net revenue:", float(monthly.iloc[-1]["net_revenue"]))
    print("Latest MoM growth:", monthly.iloc[-1]["mom_growth"])
    print("Latest YoY growth:", monthly.iloc[-1]["yoy_growth"])


if __name__ == "__main__":
    main()
