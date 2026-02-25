# Dataset Overview

## Dataset Type
Representative revenue performance dataset designed to support multi-driver analysis.

---

## Time Span
24 months of operational data.

---

## Purpose of the Dataset
To evaluate competing explanations for net revenue growth slowing by analyzing:

- Acquisition efficiency
- Retention and churn dynamics
- Pricing and discount trends
- Revenue per account changes

The dataset must allow comparison between structural drivers.

---

## Tables Included

### 1. Customer Accounts
- account_id
- industry
- acquisition_channel
- start_date
- tenure_months

### 2. Sales & Acquisition
- account_id
- acquisition_cost
- conversion_rate
- deal_size

### 3. Revenue
- account_id
- monthly_recurring_revenue
- expansion_revenue
- contraction_revenue
- discount_percentage

### 4. Retention
- account_id
- churn_flag
- churn_month

---

## Revenue Accounting Assumption (Lock This)
monthly_recurring_revenue (MRR) is treated as realized revenue after discounts.
Discount percentage is used for pricing analysis but is not reapplied to compute revenue.

Net Revenue (Monthly) = Σ (MRR + Expansion − Contraction)

---

## Key Assumptions
- Revenue slowdown may result from multiple structural drivers
- Each driver leaves measurable patterns in the data
- Framing determines which signals are prioritized

---

## Explicit Non-Goals
- Building predictive models
- Forecasting future revenue
- Optimizing marketing spend directly
- Performing granular sales funnel analysis

The objective is comparative structural diagnosis, not operational optimization.
