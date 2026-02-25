from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"


def _latest_non_null(series: pd.Series):
    s = series.dropna()
    return None if s.empty else s.iloc[-1]


def _streak_length(series: pd.Series) -> int:
    """Count consecutive identical non-null values at the end of a series."""
    s = series.dropna()
    if s.empty:
        return 0
    last = s.iloc[-1]
    n = 0
    for v in reversed(s.tolist()):
        if v != last:
            break
        n += 1
    return n


def main() -> None:
    comp = pd.read_csv(PROC / "phase3_driver_comparison.csv", parse_dates=["month"])

    # Leaders
    lever_leader = _latest_non_null(comp.get("leader_lever_3m"))
    pressure_leader = _latest_non_null(comp.get("leader_pressure_3m"))

    pressure_streak = _streak_length(comp.get("leader_pressure_3m")) if "leader_pressure_3m" in comp.columns else 0

    # Recommendation rule: declare a single dominant pressure only if it holds for >=3 consecutive months.
    if pressure_streak >= 3:
        recommendation_driver = pressure_leader
        recommendation_mode = "single-driver"
    else:
        recommendation_driver = None
        recommendation_mode = "mixed-signal"

    last6 = comp.tail(6)[[
        "month",
        "net_revenue",
        "mom_growth",
        "yoy_growth",
        "leader_lever_3m",
        "leader_pressure_3m",
        "acq_abs_3m",
        "ret_abs_3m",
        "prc_abs_3m",
        "acq_pressure_3m",
        "ret_pressure_3m",
        "prc_pressure_3m",
    ]].copy()
    last6["month"] = last6["month"].dt.strftime("%b %Y")

    md: list[str] = []
    md.append("# Phase 4 - Strategic Recommendation")
    md.append("")

    md.append("## Recommendation")
    if recommendation_mode == "single-driver":
        md.append(
            f"Primary conclusion (based on rolling 3-month pressure with >=3-month consistency): **{recommendation_driver}** is the leading structural drag in the latest window."
        )
    else:
        md.append(
            "No single driver meets the explicit consistency rule in the latest window. Treat this as a mixed-signal period and use the pressure view to prioritize near-term action."
        )

    md.append("")
    md.append("## What this means")

    if recommendation_mode == "single-driver":
        if recommendation_driver == "pricing":
            md.append("Prioritize a packaging and pricing intervention this quarter.")
            md.append("Focus on plan tier mix, seat contraction, and ARPA drift as the measurable levers.")
        elif recommendation_driver == "retention":
            md.append("Prioritize retention and expansion initiatives this quarter.")
            md.append("Focus on churn, contraction, and expansion dynamics as the measurable levers.")
        elif recommendation_driver == "acquisition":
            md.append("Prioritize acquisition output improvements this quarter.")
            md.append("Focus on new account volume, referral source mix, and starting MRR for new accounts.")
    else:
        md.append(f"Largest lever by magnitude (latest window): **{lever_leader}**.")
        md.append(f"Largest drag by directional pressure (latest window): **{pressure_leader}** (streak: {pressure_streak} months).")
        md.append("If you must pick one primary initiative under a hard constraint, prioritize the drag leader; use the lever leader as a secondary monitoring lens.")

    md.append("")
    md.append("## Evidence snapshot (last 6 months)")
    md.append("")
    md.append(last6.to_markdown(index=False))

    md.append("")
    md.append("## Interpretation and guardrails")
    md.append("- Two views are provided: **lever** (largest magnitude movement) and **pressure** (largest directional drag/headwind).")
    md.append("- Pressure is computed as headwind-only: acquisition (only negative contribution), pricing (only ARPA compression), retention (churn+contraction drag).")
    md.append("- The explicit dominance rule requires >=3 consecutive months of the same pressure leader; otherwise the window is treated as mixed-signal.")

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
