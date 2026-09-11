# Key Numbers Cheat Sheet

## Baseline Comparison (Top‑1 Accuracy)
- FT Hybrid (headline): **64.63 %**
- FT Hybrid Gated: **61.57 %**
- FT SBERT NN only: **62.88 %**
- Full CAPT‑M (Base SBERT): **51.09 %**
- MiniLM L6‑v2 Cosine NN: **51.97 %**
- Base SBERT NN: **52.84 %**
- TF‑IDF + LR: **22.27 %**

## Component Ablation (Δ Top‑1 pp)
- Stage 2 (add gated model): **‑6.11 pp**
- Stage 3 (add hybrid gating): **‑4.37 pp**
- Stage 4 (no change): **0.00 pp**
- Stage 5 (add final fine‑tuning): **‑5.68 pp**

## LOSO Generalization (Top‑1 Accuracy)
- OS: **41.05 %**
- CN: **58.06 %**
- DBMS: **51.39 %**

## Abstention‑aware Metrics
- Coverage: **91.70 %** (210/229)
- Accuracy‑on‑Covered: **67.14 %** (141/210)

## Significance Tests
- FT Hybrid vs. Baseline: **p = 0.003** (significant)
- FT Hybrid vs. MiniLM: **p = 0.021**
- FT Hybrid vs. Base SBERT: **p = 0.015**

## Bootstrap 95 % CI (Top‑1)
- FT Hybrid: **[58.24 %, 70.53 %]**
- FT Hybrid Gated: **[55.13 %, 67.63 %]**
- FT SBERT NN only: **[56.47 %, 68.83 %]**
