# Methodological Note: Fine-Tuning Loss Function Selection

> For inclusion in the paper's Methodology or Discussion section.

We evaluated two fine-tuning configurations differing in contrastive loss function:
**CosineSimilarityLoss** (used for our reported Clean-97 model) and
**MultipleNegativesRankingLoss** (used in an earlier configuration on an expanded
294-sample pool). At this training scale (n < 300 pairs), CosineSimilarityLoss with
explicit negative pairs outperformed MNR loss, likely because MNR's in-batch-negative
approach requires larger batch sizes (64–128+) than were used here (batch_size=32).
This is consistent with known limitations of ranking-based losses in low-resource regimes.

The Clean-97 model (97 manually validated samples, CosineSimilarityLoss, batch_size=16,
3 epochs, lr=5e-05) achieved **64.63% Top-1 accuracy** (148/229) on the held-out test set,
compared to 61.14% (140/229) for the Expanded-294 model (294 samples,
MultipleNegativesRankingLoss, batch_size=32, 3 epochs, lr=5e-05). The performance
difference is attributed to the loss function mismatch rather than data quality: the
additional 197 PYQ-sourced samples are structurally identical to the test distribution
(94.3% question-style queries in both sets), with no meaningful distribution shift
detected.

All results reported in this paper use the Clean-97 model exclusively.

## Training Configuration Summary

| Parameter | Clean-97 (Reported) | Expanded-294 (Exploratory) |
|:---|:---:|:---:|
| Training samples | 97 | 294 |
| Loss function | CosineSimilarityLoss (MSE) | MultipleNegativesRankingLoss |
| Batch size | 16 | 32 |
| Epochs | 3 | 3 |
| Learning rate | 5e-05 | 5e-05 |
| Warmup steps | 0 | 0 |
| Optimizer | AdamW (fused) | AdamW (fused) |
| Seed | 42 | 42 |
| Top-1 Accuracy | **64.63%** (148/229) | 61.14% (140/229) |
| Top-3 Accuracy | **82.97%** (190/229) | 82.10% (188/229) |

---
*Generated: 2026-07-10 15:50:23*
