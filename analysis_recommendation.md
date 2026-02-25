# Phase 4 - Strategic Recommendation

## Recommendation
No single driver meets the explicit consistency rule in the latest window. Treat this as a mixed-signal period and use the pressure view to prioritize near-term action.

## What this means
Largest lever by magnitude (latest window): **pricing**.
Largest drag by directional pressure (latest window): **retention** (streak: 2 months).
If you must pick one primary initiative under a hard constraint, prioritize the drag leader; use the lever leader as a secondary monitoring lens.

## Evidence snapshot (last 6 months)

| month    |   net_revenue |   mom_growth |   yoy_growth | leader_lever_3m   | leader_pressure_3m   |   acq_abs_3m |   ret_abs_3m |   prc_abs_3m |   acq_pressure_3m |   ret_pressure_3m |   prc_pressure_3m |
|:---------|--------------:|-------------:|-------------:|:------------------|:---------------------|-------------:|-------------:|-------------:|------------------:|------------------:|------------------:|
| Jul 2024 |        299373 |    0.0789888 |      7.4717  | pricing           | retention            |      10191.2 |        38015 |      68732.1 |           1955.85 |             25293 |         13843     |
| Aug 2024 |        331143 |    0.106122  |      5.55508 | acquisition       | retention            |      27497.7 |        27259 |      20991.5 |          19262.4  |             27259 |         20991.5   |
| Sep 2024 |        385689 |    0.16472   |      3.55101 | pricing           | retention            |      38530.9 |        36535 |      49636.5 |          17306.5  |             27056 |         12673.3   |
| Oct 2024 |        407520 |    0.0566026 |      3.35278 | acquisition       | acquisition          |      69166.1 |        26672 |      44968.3 |          17306.5  |             17193 |          8005.08  |
| Nov 2024 |        468207 |    0.148918  |      2.8502  | pricing           | retention            |      55240.1 |        53040 |      82335.3 |              0    |             43561 |           856.588 |
| Dec 2024 |        574643 |    0.227327  |      4.05594 | pricing           | retention            |      74939   |        82016 |      87474.4 |          32688    |             82016 |           856.588 |

## Interpretation and guardrails
- Two views are provided: **lever** (largest magnitude movement) and **pressure** (largest directional drag/headwind).
- Pressure is computed as headwind-only: acquisition (only negative contribution), pricing (only ARPA compression), retention (churn+contraction drag).
- The explicit dominance rule requires >=3 consecutive months of the same pressure leader AND a material margin (>=15%) over the runner-up; otherwise the window is treated as mixed-signal.

## Risks and limitations
- CAC and conversion are not available, so acquisition is evaluated via output and value proxies.
- Discount percentage is not available, so pricing is evaluated via ARPA drift, plan tier migration, and seat changes.
- No cost data is available, so margin is not modeled.
- Expansion and contraction are inferred from account-month MRR deltas; validate with billing event logic in a real system.
