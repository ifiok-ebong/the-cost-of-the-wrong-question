# Dataset Overview

## Dataset Type
Multi-table SaaS subscription dataset suitable for structural diagnosis of net revenue slowdown.

---

## Time Span
Multiple years of account activity (dates available in subscription, churn, usage, and support tables).

---

## Dataset Source
Kaggle dataset ref:
- `rivalytics/saas-subscription-and-churn-analytics-dataset`

License:
- MIT

---

## Purpose of the Dataset
To evaluate competing explanations for net revenue growth slowing by analyzing:
- Acquisition output signals (volume and mix)
- Retention and churn dynamics
- Pricing compression proxies (plan tier, seats, ARPA drift)

---

## Tables Included (Raw Files)

### 1. Accounts (`ravenstack_accounts.csv`)
Representative account attributes.

Key fields:
- `account_id`
- `industry`, `company_size`, `country`
- `referral_source`
- `signup_date`
- ``
- ``

### 2. Subscriptions (`ravenstack_subscriptions.csv`)
Subscription history and realized recurring revenue per subscription.

Key fields:
- `subscription_id`, `account_id`
- `start_date`, `end_date`
- `plan_tier`, `seats`
- `mrr_amount`, `arr_amount`
- `upgrade_flag`, `downgrade_flag`, `churn_flag`

### 3. Churn Events (`ravenstack_churn_events.csv`)
Churn events and reasons.

Key fields:
- `account_id`, `churn_date`
- `churn_reason`, `churn_type`

### 4. Feature Usage (`ravenstack_feature_usage.csv`) (Optional signal layer)
Behavioral usage signals.

Key fields:
- `account_id`, `usage_date`
- `feature_name`, `usage_count`, `active_users`, `session_duration_minutes`

### 5. Support Tickets (`ravenstack_support_tickets.csv`) (Optional signal layer)
Support workload and customer friction.

Key fields:
- `ticket_id`, `account_id`
- `submitted_at`, `closed_at`
- `resolution_time_hours`, `priority`, `first_response_time_minutes`

---

## Revenue Accounting Assumption (Authoritative)
Net Revenue (Monthly) is computed as the sum of realized MRR across accounts:

Net Revenue (Monthly) = sum of account-month MRR

MRR is taken from `mrr_amount` and treated as realized recurring revenue.

Discount percentage is not available in this dataset.
Pricing compression is evaluated via ARPA drift, plan tier migration, and seat changes.

---

## What Is Not Available (Documented Limitations)
- CAC
- Conversion rate
- Explicit discount percentage
- Cost data (so gross margin is not modeled)

Acquisition is evaluated using volume and value signals (new accounts, contract value, initial MRR, and channel mix).

---

## Explicit Non-Goals
- Predictive modeling
- Forecasting
- Optimization simulations

The objective is comparative structural diagnosis, not technical complexity.
