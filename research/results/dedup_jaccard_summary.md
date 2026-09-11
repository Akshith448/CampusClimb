# Deduplication Hard-Case Fix: Jaccard Secondary Check

**Method**: For borderline cosine scores [0.7, 0.8], require both cosine ≥ 0.75 AND Jaccard ≥ 0.25 to classify as duplicate.

**Jaccard threshold** tuned on 30-pair dev set; evaluated on 60-pair held-out eval set.

## Full Eval Set (60 pairs)

| Metric | Baseline (cosine only) | Jaccard Fix | Change |
|:---|:---:|:---:|:---:|
| Precision | 0.5400 | 0.6452 | +0.1052 |
| Recall    | 1.0000  | 0.7407  | -0.2593  |
| F1        | 0.7013   | 0.6897   | -0.0116   |
| TP/FP/FN/TN | 27/23/0/10 | 20/11/7/22 | — |

## Hard-Case Subset (40 near-threshold pairs)

| Metric | Baseline | Jaccard Fix | Change |
|:---|:---:|:---:|:---:|
| Precision | 0.4250 | 0.4762 | +0.0512 |
| Recall    | 1.0000  | 0.5882  | -0.4118  |
| F1        | 0.5965   | 0.5263   | -0.0702   |
| **TNR (key)** | **0.00%** (0/23) | **52.17%** (12/23) | **+52.17pp** |
| TP/FP/FN/TN | 17/23/0/0 | 10/11/7/12 | — |