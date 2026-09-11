# RESULTS_TABLES.md

## Table I: Baseline Comparison (Top‑1 / Top‑3 / Macro F1 / 95% CI)

| Method | Top‑1 Accuracy | Top‑1 95% CI | Top‑3 Accuracy | Macro F1 |
|---|---|---|---|---|
| TF‑IDF + Logistic Regression | 22.27 % (51/229) | [17.36 %, 28.09 %] | 37.55 % (86/229) | 0.1361 |
| all‑MiniLM‑L6‑v2 Cosine NN | 51.97 % (119/229) | [45.52 %, 58.35 %] | 72.05 % (165/229) | 0.4214 |
| Base SBERT NN (all‑mpnet‑base‑v2) | 52.84 % (121/229) | [46.38 %, 59.21 %] | 72.49 % (166/229) | 0.4312 |
| Full CAPT‑M Pipeline (Base SBERT) | 51.09 % (117/229) | [44.65 %, 57.49 %] | 61.14 % (140/229) | 0.4667 |
| FT SBERT NN only (Clean‑97) | 62.88 % (144/229) | [56.47 %, 68.83 %] | 77.73 % (178/229) | 0.4941 |
| FT Hybrid (Clean‑97) **(headline)** | **64.63 %** (148/229) | **[58.24 %, 70.53 %]** | **82.97 %** (190/229) | **0.5482** |
| FT Hybrid Gated (Clean‑97) | 61.57 % (141/229) | [55.13 %, 67.63 %] | – | – |

*Caption: Baseline performance comparison across seven methods on the 229‑sample held‑out test set.*

---

## Table II: LOSO Generalization (per subject and aggregate)

| Target Subject | Top‑1 Accuracy | Top‑1 95% CI | Top‑3 Accuracy | n_test |
|---|---|---|---|---|
| Operating Systems | 41.05 % | [31.70 %, 51.10 %] | 46.32 % | 95 |
| Computer Networks | 58.06 % | [45.67 %, 69.52 %] | 74.19 % | 62 |
| DBMS | 51.39 % | [40.07 %, 62.57 %] | 61.11 % | 72 |
| **Aggregate Mean** | **50.17 %** | – | **60.54 %** | 229 |

*Caption: Leave‑One‑Subject‑Out (LOSO) generalization results; each row reports performance when the indicated subject is held out of training.*

---

## Table III: Component Ablation (Top‑1 Δ, Top‑3 Δ, Macro F1)

| Stage | Top‑1 Accuracy | Δ pp (vs. previous) | Top‑3 Accuracy | Δ pp (vs. previous) | Macro F1 |
|---|---|---|---|---|---|
| 1. FT SBERT NN only | 62.88 % | – | 77.73 % | – | 0.4941 |
| 2. + complete‑linkage clustering | 56.77 % | -6.11 | 77.29 % | -0.44 | 0.4324 |
| 3. + keyword mixed‑topic detection | 52.40 % | -4.37 | 70.31 % | -6.98 | 0.4647 |
| 4. + confidence/adaptive threshold | 52.40 % | 0.00 | 71.18 % | +0.87 | 0.4658 |
| 5. + TF‑IDF hybrid stacking | 46.72 % | -5.68 | 59.83 % | -11.35 | 0.4198 |

*Caption: Ablation study showing incremental impact of each pipeline component on Top‑1, Top‑3, and macro‑F1 metrics.*

---

## Table IV: Abstention‑Aware Metrics

| Metric | Value | Numerator | Denominator | Description |
|---|---|---|---|---|
| Coverage | 91.70 % | 210 | 229 | Percentage of samples receiving a topic assignment |
| Accuracy on Covered | 67.14 % | 141 | 210 | Top‑1 accuracy restricted to covered samples |
| Raw Accuracy (abstentions = incorrect) | 61.57 % | 141 | 229 | Overall Top‑1 accuracy when abstentions counted as wrong |

**Per‑Subject Abstention Rates**

| Subject | Abstention Rate | Abstained | Total |
|---|---|---|---|
| Operating Systems | 9.47 % | 9 | 95 |
| Computer Networks | 4.84 % | 3 | 62 |
| DBMS | 9.72 % | 7 | 72 |

*Caption: Metrics that account for the gated (abstention‑enabled) model’s coverage and accuracy.*

---

## Table V: McNemar Significance Tests

| Comparison | χ² Statistic | p‑value | Discordant (b / c) | Odds Ratio | Cohen’s g | Significant? |
|---|---|---|---|---|---|---|
| FT Hybrid vs. SBERT NN (base) | 18.6923 | **1.54e‑05** | 33 / 6 | 5.1538 | 0.3462 | **YES** |
| CAPT‑M FT ST vs. CAPT‑M Base ST | 22.0000 | **2.73e‑06** | 22 / 0 | 45.0 | 0.5000 | **YES** |
| FT Hybrid vs. MiniLM NN | 20.5122 | **5.93e‑06** | 35 / 6 | 5.4615 | 0.3537 | **YES** |

*Caption: McNemar’s test results assessing statistical significance of performance gains.*

---

## Table VI: Bootstrap Confidence Intervals (pairwise)

| Comparison | Mean Accuracy Δ | 95 % CI Lower | 95 % CI Upper |
|---|---|---|---|
| FT Hybrid vs. Base SBERT NN | 0.1194 | 0.0655 | 0.1747 |
| FT Hybrid vs. MiniLM NN | 0.1270 | 0.0741 | 0.1834 |
| FT Hybrid vs. TF‑IDF alone | 0.1438 | 0.0917 | 0.1965 |
| FT Hybrid vs. TF‑IDF + Logistic Regression | 0.4221 | 0.3493 | 0.4978 |

*Caption: Paired bootstrap confidence intervals for pairwise accuracy differences (1000 resamples).*
