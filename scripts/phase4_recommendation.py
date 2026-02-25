from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"


def main() -> None:
    comp = pd.read_csv(PROC / "phase3_driver_comparison.csv", parse_dates=["month"])

    # Determine dominant driver based on latest non-null leader_3m
    latest = comp.dropna(subset=["leader_3m"]).iloc[-1]
    dominant = latest["leader_3m"]

    # Basic evidence snippets
    last6 = comp.tail(6)[["month", "net_revenue", "mom_growth", "yoy_growth", "leader_3m", "acq_abs_3m", "ret_abs_3m", "prc_abs_3m"]]

    last6 = last6.copy()
    last6["month"] = last6["month"].dt.strftime("%b %Y")

    md = []
    md.append("# Phase 4 - Strategic Recommendation")
    md.append("")
    md.append(f"## Recommendation")
    md.append(f"Primary conclusion (based on rolling 3-month impact): **{dominant}** is the leading structural pressure in the latest window.")
    md.append("")
    md.append("## What this means")

    if dominant == "pricing":
        md.append("Prioritize a packaging and pricing intervention this quarter.")
        md.append("Focus on plan tier mix, seat contraction, and ARPA drift as the measurable levers.")
    elif dominant == "ltv":
        md.append("Prioritize retention and expansion initiatives this quarter.")
        md.append("Focus on churn, contraction, and expansion dynamics as the measurable levers.")
    elif dominant == "acquisition":
        md.append("Prioritize acquisition output improvements this quarter.")
        md.append("Focus on new account volume, referral source mix, and starting MRR for new accounts.")
    else:
        md.append("No single dominant driver could be established in the latest window.")
        md.append("A dual-driver recommendation may be more defensible.")

    md.append("")
    md.append("## Evidence snapshot (last 6 months)")
    md.append("")
    md.append(last6.to_markdown(index=False))

    md.append("")
    md.append("## Risks and limitations")
    md.append("- CAC and conversion are not available, so acquisition is evaluated via output and value proxies.")
    md.append("- Discount percentage is not available, so pricing is evaluated via ARPA drift, plan tier migration, and seat changes.")
    md.append("- No cost data is available, so margin is not modeled.")
    md.append("- Expansion and contraction are inferred from account-month MRR deltas; validate with billing event logic in a real system.")

    out_path = ROOT / "analysis_recommendation.md"
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
