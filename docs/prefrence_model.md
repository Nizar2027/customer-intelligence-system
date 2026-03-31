
## Preference Modeling — Customer Intelligence System

### Objective

The goal of this component is to model **customer preferences** by identifying and ranking the products that each customer is most likely interested in.

Unlike churn prediction and revenue forecasting, this task does **not rely on supervised learning**, since there is no explicit target label.
Instead, we use a **behavior-driven scoring and ranking approach**.

---

## Problem Framing

We aim to answer the question:

> *"Which products does each customer truly prefer?"*

To achieve this, we rely entirely on **historical transaction behavior**, specifically:

* How often a product is purchased (frequency)
* How much is spent on it (monetary value)
* How recently it was purchased (recency)

---

## Initial Approach (Heuristic Scoring)

We started with a simple weighted scoring formula:

```
preference_score = 0.5 * frequency + 0.3 * monetary + 0.2 * recency
```

This approach was:

* Simple and interpretable
* Easy to implement
* A good starting point for ranking products

However, it had a major limitation:

> The weights were manually chosen and not based on actual data patterns.

---

## Transition to Data-Driven Weights

To improve the model, we attempted to learn the weights from data using a regression model.

### Idea:

Use **future revenue** as a proxy for customer value:

```
future_revenue = w1 * frequency + w2 * monetary + w3 * recency
```

The learned coefficients were then used as weights.

---

## Issue Discovered

The learned weights were heavily biased toward **monetary value**.

Example outcome:

* Monetary ≫ Frequency ≫ Recency

This happened because:

> The model was optimized for predicting revenue, not preference.

### Key Insight:

* Revenue emphasizes **spending**
* Preference emphasizes **repeated behavior**

This revealed a mismatch between:

* Model objective (revenue)
* Business goal (preference)

---

## Hybrid Solution (Best Practice)

To address this, we adopted a **hybrid approach**:

* Combine **model-driven weights** (data signal)
* With **manual weights** (business logic)

```
final_weights = 0.3 * w_model + 0.7 * w_manual
```

Final tuned weights:

* Frequency ≈ 0.47
* Monetary ≈ 0.42
* Recency ≈ 0.10

This provided a balanced and interpretable scoring system.

---

## Second Issue: Global Normalization

The initial implementation used global normalization (MinMaxScaler across all customers).

This caused a major problem:

* Customers with extreme spending (outliers) distorted the scale
* Other customers’ values were compressed near zero
* Ranking became unfair across customers

---

## Final Improvement: Customer-Level Normalization

To fix this, we switched to **per-customer normalization**:

* Each customer's products are normalized within their own context
* Eliminates cross-customer interference
* Produces fair and meaningful rankings

### Additional Enhancement:

* Applied `log1p()` transformation to monetary values to reduce the impact of outliers

---

## Final Pipeline

The final preference modeling pipeline consists of:

1. Data Cleaning

   * Remove missing customers
   * Remove returns (negative quantities)

2. Feature Engineering

   * Frequency (number of purchases)
   * Monetary (total spending)
   * Recency (days since last purchase)

3. Transformation

   * Log transform for monetary
   * Per-customer normalization

4. Scoring

```
preference_score =
    w_freq * freq_norm +
    w_monetary * monetary_norm +
    w_recency * recency_norm
```

5. Ranking

   * Sort products per customer by score

---

## Final Output

The result is a dataset containing:

* CustomerID
* Product (Description)
* Preference Score

Sorted per customer, enabling:

* Top-N product recommendations
* Customer-level insights
* Integration with downstream systems

---

## Key Learnings

* Preference modeling is fundamentally different from supervised ML
* Feature scaling strategy significantly impacts ranking quality
* Data-driven methods must align with business objectives
* Hybrid approaches often outperform purely manual or purely automated methods

---

## ✅ Conclusion

We successfully built a **production-ready preference modeling system** that:

* Accurately reflects customer behavior
* Produces meaningful rankings
* Aligns with real business use cases

This completes the third core component of the Customer Intelligence System.
