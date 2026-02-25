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

## Revenue Definition

Net Revenue (Monthly) = Σ (MRR + Expansion − Contraction)

### Revenue Accounting Assumption
monthly_recurring_revenue (MRR) is treated as realized revenue after discounts.
Discount percentage is used for pricing analysis but is not reapplied to compute net revenue.

Lock this definition once. Do not deviate.

---

## Time Alignment Rules (Authoritative Defaults)

These rules exist to prevent off-by-one errors and circular accounting.

1) Churn impact timing
- If an account churns in month t (churn_month = t), its churn impact is measured as the **prior month** realized MRR (month t−1) that no longer recurs.
- Rationale: churn-month MRR may be recorded as 0, which would understate impact.

2) Expansion and contraction timing
- expansion_revenue and contraction_revenue are treated as **in-month deltas** and included directly in Net Revenue for month t.

3) New account “starting MRR”
- Starting MRR for a new account is defined as its **first observed realized MRR** in its first active revenue month.

---

# Phase 1  -  Establish Revenue Baseline

## Step 1: Confirm Net Revenue Slowdown Exists

Compute:
- Total monthly net revenue (24 months)
- Net revenue growth rate (MoM and YoY)
- Net revenue trend

Objective:
Verify that slowdown is structural and not a short-term anomaly.

If slowdown is not directionally evident,
the premise of the analysis must be re-evaluated.

---

# Phase 2  -  Independent Hypothesis Evaluation

Each structural driver is evaluated independently
before any comparison occurs.

---

## Hypothesis A: Acquisition Efficiency Decline

### Step 2A.1  -  Evaluate Customer Acquisition Cost (CAC)

- Trend over 24 months
- Rate of increase
- Volatility patterns

Question:
Has CAC increased materially relative to historical baseline?

---

### Step 2A.2  -  Evaluate Conversion Rate

- Conversion trend by acquisition channel
- Drop magnitude over time

Question:
Is conversion efficiency deteriorating consistently?

---

### Step 2A.3  -  Evaluate New Account Volume

- New accounts per month
- Growth or decline trajectory

Question:
Is acquisition output declining?

---

### Step 2A.4  -  Optional Context: CAC-to-LTV

Do not treat CAC-to-LTV as decision-critical unless LTV can be computed credibly.
If used, present as directional context only.

Decision Marker:
If acquisition efficiency metrics show sustained deterioration
that plausibly explains the net revenue slowdown magnitude,
Hypothesis A remains viable.

Otherwise, it weakens.

---

## Hypothesis B: Lifetime Value Deterioration

### Step 2B.1  -  Evaluate Churn

- Overall churn trend
- Tenure-segmented churn
- Acceleration patterns

Question:
Is churn increasing structurally?

---

### Step 2B.2  -  Evaluate Net Revenue Retention (NRR)

- Trend over time
- Contribution of expansion vs contraction

Question:
Is customer value decaying post-acquisition?

---

### Step 2B.3  -  Evaluate Expansion Revenue

- Expansion growth vs historical baseline
- Segment-level differences

Question:
Has expansion momentum slowed materially?

---

### Step 2B.4  -  Evaluate Contraction & Downgrade Patterns

- Frequency of downgrades
- Revenue loss from contraction

Decision Marker:
If LTV-related metrics show sustained negative pressure
that aligns with slowdown magnitude,
Hypothesis B remains viable.

Otherwise, it weakens.

---

## Hypothesis C: Pricing Compression

### Step 2C.1  -  Evaluate Discount Trends

- Average discount percentage over time
- Variance by segment

Question:
Has discounting increased materially?

---

### Step 2C.2  -  Evaluate ARPA (Average Revenue Per Account)

- Trend over time
- Interpreted alongside churn

Question:
Is per-account realized revenue declining independent of churn?

---

### Step 2C.3  -  Evaluate Effective Revenue Yield (No Cost Data)

Replace “gross margin trend” with a measurable pricing signal:
- ARPA trend
- Discount percentage trend
- Relationship between rising discount% and ARPA decline

Decision Marker:
If ARPA declines and discounting increases independent of churn or acquisition,
Hypothesis C remains viable.

Otherwise, it weakens.

---

# Phase 3  -  Structural Comparison

Only after all three hypotheses are evaluated independently.

---

## Step 3.1  -  Quantify Relative Impact (Simple Decomposition)

Decompose net revenue change into three additive components.

1) Acquisition contribution (volume-driven)
- Approximate as: Δ New Accounts × Avg Starting MRR

2) Retention / LTV contribution (post-acquisition decay)
- Approximate as: Δ Churned Revenue + Δ Contraction − Δ Expansion

3) Pricing contribution (pricing compression)
- Approximate as: Δ ARPA attributable to discount% change
  (assessed via ARPA trend, discount% trend, and their relationship)

Each hypothesis must be summarized using:
1. Magnitude of impact
2. Consistency over time
3. Breadth of revenue affected
4. Structural persistence

---

## Step 3.2  -  Dominance Assessment (Explicit Rule)

A driver is considered dominant if:
- Its revenue impact magnitude exceeds the others by a material margin (target: >15–20%), and
- The direction of change is consistent over at least 3 consecutive months.

If two drivers are within ~10% impact magnitude and show correlated deterioration,
state explicitly that the slowdown is dual-driver.

---

# Phase 4  -  Strategic Recommendation

## Step 4.1  -  Translate Dominant Driver Into Action

Map dominant driver to strategic intervention:
- Acquisition → Marketing optimization
- LTV → Retention & expansion focus
- Pricing → Packaging & pricing intervention

---

## Step 4.2  -  Risk Acknowledgment

Explicitly state:
- What this analysis does not capture
- What assumptions may bias results
- Where uncertainty remains

---

# Completion Criteria

The blueprint is successfully executed when:
- Each hypothesis is evaluated independently
- No hypothesis is prematurely dismissed
- One structural driver is defensibly dominant OR
- A multi-driver reality is clearly articulated

The analysis must be explainable verbally in under three minutes.

---

# Guardrails

Stop analysis if:
- You begin optimizing one driver before comparison is complete
- You add metrics outside defined categories
- You attempt to over-quantify beyond decision relevance

This project exists to demonstrate disciplined structural diagnosis,
not technical complexity.

---

End of Analysis Execution Blueprint
