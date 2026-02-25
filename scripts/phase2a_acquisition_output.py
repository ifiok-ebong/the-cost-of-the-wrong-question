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
    accounts["signup_date"] = pd.to_datetime(accounts["signup_date"], errors="coerce")

    account_month = pd.read_csv(PROC / "account_month_mrr.csv")
    account_month["month"] = pd.to_datetime(account_month["month"], errors="coerce")

    # New accounts per month
    accounts = accounts.dropna(subset=["account_id", "signup_date"]).copy()
    accounts["signup_month"] = month_floor(accounts["signup_date"])

    new_accounts = (
        accounts.groupby("signup_month", as_index=False)
        .agg(new_accounts=("account_id", "nunique"))
        .sort_values("signup_month")
        .rename(columns={"signup_month": "month"})
    )

    # Referral source mix by month
    mix = (
        accounts.groupby(["signup_month", "referral_source"], as_index=False)
        .agg(new_accounts=("account_id", "nunique"))
        .sort_values(["signup_month", "new_accounts"], ascending=[True, False])
        .rename(columns={"signup_month": "month"})
    )

    # Initial MRR for new accounts (first observed account-month MRR)
    first_mrr = (
        account_month.sort_values(["account_id", "month"])
        .groupby("account_id", as_index=False)
        .first()[["account_id", "month", "mrr_amount"]]
        .rename(columns={"month": "first_mrr_month", "mrr_amount": "starting_mrr"})
    )

    # Join to accounts and aggregate starting MRR by signup month
    joined = accounts.merge(first_mrr, on="account_id", how="left")
    starting = (
        joined.groupby("signup_month", as_index=False)
        .agg(
            avg_starting_mrr=("starting_mrr", "mean"),
            median_starting_mrr=("starting_mrr", "median"),
            pct_missing_starting_mrr=("starting_mrr", lambda s: float(s.isna().mean())),
        )
        .sort_values("signup_month")
        .rename(columns={"signup_month": "month"})
    )

    # Save outputs
    new_accounts.to_csv(PROC / "hypA_new_accounts_per_month.csv", index=False)
    mix.to_csv(PROC / "hypA_referral_source_mix.csv", index=False)
    starting.to_csv(PROC / "hypA_starting_mrr_trend.csv", index=False)

    # Tight printout
    print("New accounts months:", new_accounts["month"].min(), "to", new_accounts["month"].max())
    print("Total new accounts:", int(new_accounts["new_accounts"].sum()))
    print("Starting MRR missing pct (avg):", float(starting["pct_missing_starting_mrr"].mean()))


if __name__ == "__main__":
    main()
