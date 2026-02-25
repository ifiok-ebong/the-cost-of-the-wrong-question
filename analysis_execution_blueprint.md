# Analysis Execution Blueprint
The Cost of the Wrong Question

---

## Purpose
This blueprint defines the exact order in which hypotheses will be evaluated.

The objective is to:
- Prevent narrative bias
- Avoid premature conclusions
- Ensure structural comparison across drivers

No hypothesis may be dismissed before full evaluation.

This document serves as the pre-registered analytical sequence to prevent narrative bias and post-hoc justification.

---

## Revenue Definition (Authoritative)
Net Revenue (Monthly) = sum of account-month MRR

MRR is taken from `mrr_amount` and treated as realized recurring revenue.

---

## Time Alignment Rules (Authoritative Defaults)
1) Churn impact timing
- If an account churns in month t, churn impact is measured as the prior month realized MRR (t-1) that no longer recurs.

2) Expansion and contraction timing
- Expansion and contraction are measured via changes in account-month MRR, supported by upgrade and downgrade flags.

3) New account starting MRR
- Starting MRR is defined as first observed realized MRR in the first active revenue month.

---

# Phase 1 - Establish Revenue Baseline

## Step 1: Confirm Net Revenue Slowdown Exists
Compute:
- Total monthly net revenue (24 months)
- Net revenue growth rate (MoM and YoY)
- Net revenue trend

Objective:
Verify slowdown is structural and not a short-term anomaly.

---

# Phase 2 - Independent Hypothesis Evaluation
Each structural driver is evaluated independently before comparison.

---

## Hypothesis A: Acquisition Output Decline

### Step 2A.1 - Evaluate New Account Volume
- New accounts per month (from `signup_date`)
- Trend and volatility

Question:
Is acquisition output declining structurally?

---

### Step 2A.2 - Evaluate Contract Value and Initial MRR
- Starting MRR trend for new accounts (first observed realized MRR)
- Initial MRR trend for new accounts

Question:
Are new accounts arriving with lower value?

---

### Step 2A.3 - Evaluate Channel Mix
- Referral source mix shift over time (from `referral_source`)

Question:
Is mix shifting toward lower-value channels?

Decision Marker:
If acquisition output and value signals deteriorate in a sustained way and plausibly explain slowdown magnitude, Hypothesis A remains viable.

---

## Hypothesis B: Customer Lifetime Value Deterioration

### Step 2B.1 - Evaluate Churn
- Overall churn trend
- Tenure-segmented churn

Question:
Is churn increasing structurally?

---

### Step 2B.2 - Evaluate Expansion vs Contraction
- Expansion and contraction patterns inferred from account-month MRR deltas
- Upgrade vs downgrade flags as supporting evidence

Question:
Is customer value decaying post-acquisition?

Decision Marker:
If post-acquisition decay aligns with slowdown magnitude, Hypothesis B remains viable.

---

## Hypothesis C: Pricing Compression (Proxies)

### Step 2C.1 - Evaluate ARPA Drift
- ARPA trend over time

Question:
Is per-account realized revenue declining independent of churn?

---

### Step 2C.2 - Evaluate Plan Tier and Seat Migration
- Plan tier mix shift over time
- Seat changes over time

Question:
Is pricing compression occurring via down-tiering or seat contraction?

Decision Marker:
If ARPA declines with plan mix shifts and seat contraction independent of churn or acquisition, Hypothesis C remains viable.

---

# Phase 3 - Structural Comparison

## Step 3.1 - Quantify Relative Impact (Simple Decomposition)
Decompose net revenue change into additive components (practical heuristic using available fields):

1) Acquisition contribution
- Approximate as: delta new accounts x average starting MRR

2) Retention contribution
- Approximate as: churned MRR + contraction MRR - expansion MRR

3) Pricing contribution
- Approximate as ARPA drift attributable to plan tier and seat migration

Note: these components are not guaranteed to be mutually exclusive in this dataset; the goal is comparative diagnosis, not perfect attribution.

Note: the Phase 3 "leader" is evaluated on rolling 3-month *magnitude* of movement to identify the biggest lever; interpret with direction and context.

Summarize each driver by:
- Magnitude of impact
- Consistency over time
- Breadth of revenue affected
- Structural persistence

---

## Step 3.2 - Dominance Assessment (Explicit Rule)
A driver is dominant if:
- Its impact exceeds others by a material margin (>15-20%), and
- Direction is consistent over at least 3 consecutive months.

If two drivers are within ~10% and correlated, state a dual-driver conclusion.

---

# Phase 4 - Strategic Recommendation

## Step 4.1 - Translate Dominant Driver Into Action
Map dominant driver to intervention:
- Acquisition output -> acquisition strategy and channel focus
- LTV -> retention and expansion focus
- Pricing compression -> packaging and pricing intervention

---

## Step 4.2 - Risk Acknowledgment
Explicitly state:
- What this analysis does not capture
- Where uncertainty remains

---

End of Analysis Execution Blueprint
