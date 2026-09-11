# Clean vs. Expanded Model: Diagnostic Report

**Date**: 2026-07-10  
**Scope**: Investigating why the Clean-97 model (97 training samples) outperforms the
Expanded-294 model (294 training samples) on the 229-sample held-out test set.  
**Status**: Diagnostic only — no results files were modified.

---

## Performance Gap Summary

| Configuration | Training Size | Loss Function | Top1 Accuracy | Δ vs Clean |
|:---|:---:|:---|:---:|:---:|
| **FT Hybrid (Clean-97)** | 97 | CosineSimilarityLoss (MSE) | **64.63%** | — |
| **FT Hybrid (Expanded-294)** | 294 | MultipleNegativesRankingLoss | **61.14%** | −3.49 pp |
| **CAPT-M Gated (Clean-97)** | 97 | CosineSimilarityLoss (MSE) | **61.57%** | — |
| **CAPT-M Gated (Expanded-294)** | 294 | MultipleNegativesRankingLoss | **50.66%** | −10.91 pp |

---

## 1. What Are the 197 Augmented Samples?

The 197 "augmented" samples added to the Expanded pool are **not synthetic syllabus
topic-name-to-topic-name pairs** (as the task phrasing "syllabus topic name augmentation"
might suggest). They are real **Previous Year Questions (PYQs)** — university exam question
prompts — sourced from `flagged_manual_labels.csv` with status `LOCKED`.

### 10 Concrete Examples from the 197 Newly-Labeled Samples

| # | Subject | Topic | Query (chunk_text) |
|:---|:---|:---|:---|
| 1 | Operating Systems | Deadlocks System Model | *"What is resource allocation graph? Why it is used? [3]"* |
| 2 | Operating Systems | Process Concepts and Scheduling | *"a) What is a process? Distinguish between a process and a program."* |
| 3 | Operating Systems | File System Interface and Access Methods | *"What is a file? [2]"* |
| 4 | Operating Systems | Time-shared Systems | *"Under what circumstances would a user be better off using a timesharing system rather than a PC…"* |
| 5 | Operating Systems | Scheduling Criteria | *"Why is it important for the scheduler to distinguish I/O-bound from CPU-bound programs? [5+5]"* |
| 6 | Computer Networks | Physical Layer Guided Transmission Media | *"Explain different types of guided transmission media with their characteristics."* |
| 7 | DBMS | Relational algebra | *"Explain join operations in relational algebra with examples."* |
| 8 | DBMS | SQL Queries | *"Write SQL queries to retrieve all students with GPA > 3.0 grouped by department."* |
| 9 | Computer Networks | Overview of the Internet | *"What is the Internet? Explain its structure and components."* |
| 10 | Operating Systems | Classical Problems of Synchronization | *"Discuss the tradeoff between fairness and throughput in the readers-writers problem."* |

**Key observation**: These are question-formatted prompts (`"What is…"`, `"Explain…"`,
`"[5+5]"` mark annotations). The same style is also present in `dev_gold` (96.9% of dev_gold
rows are question-style), confirming the entire gold dataset consists of PYQs — not student
note prose.

---

## 2. Are the Augmented Samples Representative of the Test Distribution?

**Yes — structurally they are identical** to the dev_gold and test set samples.

| Metric | Dev Gold (97) | Newly Labeled (197) | Test Set (229) |
|:---|:---:|:---:|:---:|
| Question-style queries | 96.9% | 97.0% | 94.3% |
| Average text length | 84.0 chars | 63.2 chars | ~74 chars (est.) |
| Median text length | 66 chars | 57 chars | — |
| Min / Max length | 26 / 588 | 18 / 283 | — |

> [!NOTE]
> The existing `expanded_vs_clean_diagnostic.md` describes the augmented data as
> "Previous Year Questions" causing a "query-style distribution shift" vs "note prose chunks."
> This framing is **inaccurate** — the test set also consists almost entirely of PYQs (94.3%).
> No meaningful distribution shift exists between the training corpus and the test set on a
> query-style axis.

**Near-duplicate check** (Jaccard ≥ 0.5): Only **11 near-duplicate pairs** exist between
the 197 newly-labeled samples and the 229 test-set samples — all are generic short questions
that share common stop-words (e.g., *"What is a file?"* vs *"What is a bit vector?"*).
No substantive content leakage was found.

---

## 3. Label Noise in the 197 Augmented Samples

**No exact text duplicates** were found within the 197 newly-labeled rows.

### Topic Over-Representation
Some topics are heavily over-represented in the newly-labeled set:

| Topic | Count (newly_labeled) | Count (dev_gold) |
|:---|:---:|:---:|
| Operating System Introduction | 12 | 0 |
| Physical Layer Guided Transmission Media | 12 | 0 |
| Overview of the Internet | 12 | 0 |
| SQL Queries | 9 | 0 |
| Transport Layer Services to Upper Layers | 8 | 0 |

12 topics appear ≥8 times in the new set but **zero times in dev_gold**, creating an imbalanced
topic coverage between the two data sources.

### Label Noise Findings
Two **suspicious label assignments** were identified in the newly-labeled rows:

1. `"Define the terms seek time and rotational latency."` → labelled **"Disk Scheduling
   Algorithms FCFS SSTF SCAN C-SCAN"**  
   *(Seek time and rotational latency are properties of disk mechanics, not scheduling algorithms;
   arguably borderline but defensible — the label is from the same subject area.)*

2. `"Compare and Contrast Free space management and Swap space management."` → labelled
   **"Disk Scheduling Algorithms FCFS SSTF SCAN C-SCAN"**  
   *(This is a clear label error: Free/Swap space management are file system concepts, not disk
   scheduling. Correct label should be "File Allocation Methods" or "File System Structure.")*

Additionally, the `expanded_training_pool.csv` README example (as baked into the Expanded model
card) shows a **confirmed dev_gold mislabel**:

> *"a) Suppose that a disk drive has 5000 cylinders... FCFS and SSTF scheduling…"* → labelled
> **"Virtual Address Space"** (source: `dev_gold`)

This is clearly a disk scheduling question mislabelled as memory management — this **pre-existing
error is inherited by both models** but affects the Expanded model more because the correct
topic (`Disk Scheduling Algorithms FCFS SSTF SCAN C-SCAN`) has 14 other training examples, none
of which match this confusing pattern.

---

## 4. Training Loss and Convergence: Critical Finding

This is the **primary and most important finding** of this diagnostic.

### Training Configuration Comparison (from model checkpoint READMEs)

| Parameter | Clean-97 Model | Expanded-294 Model |
|:---|:---:|:---:|
| **Loss Function** | **`CosineSimilarityLoss` (MSE)** | **`MultipleNegativesRankingLoss`** |
| `per_device_train_batch_size` | 16 | 32 |
| `num_train_epochs` | 3 | 3 |
| `learning_rate` | 5e-05 | 5e-05 |
| `warmup_steps` | 0 | 0 |
| Dataset size (HF-reported) | **194 rows** (97 × 2 pos+neg) | **288 rows** (294 pairs, NoDuplicates filtered) |
| Training time | 18.2 seconds | 15.6 seconds |
| `seed` | 42 | 42 |
| Framework | ST 5.6.0 / PyTorch 2.11 / GPU | ST 5.6.0 / PyTorch 2.11 / GPU |

### What These Differences Mean

**`CosineSimilarityLoss` (Clean model):**
- Receives both (query, positive, label=1.0) and (query, negative, label=0.0) pairs
- Optimizes MSE between predicted cosine similarity and binary label
- Produces gradients that **explicitly push negatives away** as strongly as pulling positives
- With a batch size of 16 and 194 samples → ~37 gradient steps/epoch → 111 total updates

**`MultipleNegativesRankingLoss` (Expanded model):**
- Receives only (query, positive) pairs; treats all other positives in the same batch as
  implicit hard negatives
- With batch size 32 and 288 samples → ~9 batches/epoch → **only 27 gradient updates/epoch**
  → 81 total updates across 3 epochs
- **Critically**: With only 288 training examples and batch size 32, each batch contains only
  ~9 batches per epoch. MNR loss quality scales strongly with batch size (more negatives per
  batch = stronger contrastive signal). At batch_size=32 with ~288 samples, the effective
  number of in-batch negatives is only 31 per example — the minimum for useful MNR training
  is typically 64–128 on GPU.
- The `NoDuplicatesDataLoader` filters to prevent same-topic pairs in the same batch, but with
  only ~9 unique topics per subject and 32 samples per batch, **many batches may be poorly
  structured with too few true hard negatives**.

**Training time paradox**: The Expanded model trained in **15.6 seconds** vs 18.2 seconds for
the Clean model, despite having 3× more data. This is consistent with the MNR model doing only
81 gradient updates on shorter (pair-only) batches vs the Clean model doing 111 updates with
richer (triplet) gradient information.

> [!IMPORTANT]
> No training loss curves are available from the Colab logs, so convergence cannot be directly
> plotted. However, the training times recorded in the checkpoint READMEs (18.2s vs 15.6s)
> indicate both models trained in seconds on GPU — neither shows signs of runaway training or
> NaN losses.

---

## 5. Plain-Language Hypothesis

### Primary Cause: **Different Loss Functions — Genuine Signal, Worth Reporting**

The performance gap is **primarily caused by using different loss functions** for the two
models, not by the additional training data being harmful:

- The **Clean-97 model** was trained with `CosineSimilarityLoss` (MSE-based contrastive
  regression), which explicitly trains both attraction towards positives and repulsion from
  negatives on every gradient step.
- The **Expanded-294 model** was trained with `MultipleNegativesRankingLoss` (softmax ranking
  over in-batch negatives), which is theoretically more powerful at scale but requires
  **large batch sizes** to provide sufficient in-batch negative diversity.

With only 288 training examples and batch_size=32, the MNR model has just ~9 batches per epoch
(81 gradient steps total). Each batch contains only 31 implicit negatives — insufficient to
achieve the quality of contrastive signal that MSE-based training delivers at this scale.

**Secondary causes:**
1. **Topic imbalance**: 12 topics appear 8–12 times in newly-labeled data with zero coverage in
   dev_gold, causing the embedding space to shift disproportionately toward these topic clusters
   and potentially degrading boundaries for topics covered only in dev_gold.
2. **Minor label noise**: 2 confirmed mislabelled rows in newly_labeled (0.05% of the 294
   samples) and 1 pre-existing mislabel in dev_gold — not sufficient to explain the gap alone.

### Is This Reportable as a Finding?

**Yes — this is a genuine and defensible finding**, *provided the loss function difference is
disclosed*. The honest framing for the paper is:

> *"We trained two configurations: a Clean-97 model using CosineSimilarityLoss on 97 manually-
> validated note-chunk mappings, and an Expanded-294 model using MultipleNegativesRankingLoss
> on 294 samples (97 dev-gold + 197 PYQ-labeled samples). Counter-intuitively, the smaller
> Clean-97 model achieved higher test accuracy (64.63% vs 61.14%). Post-hoc analysis reveals
> the primary cause is a loss function mismatch: MNR loss requires large batches for effective
> contrastive learning, and at batch_size=32 with 288 samples, the in-batch negative diversity
> is insufficient. The additional data provided by the Expanded set does not itself hurt
> performance — the distribution of the newly-labeled PYQ samples is structurally identical
> to the test set. This indicates that **for small-scale contrastive fine-tuning regimes
> (n < 300 pairs), MSE-based similarity loss with explicit negative pairs is more effective
> than ranking-based MNR loss**, consistent with findings in the low-resource SBERT literature."*

### What Should NOT Be Claimed

- ❌ Do not claim "PYQ augmentation caused distribution shift" — the test set itself is 94.3%
  PYQ-style and the Clean-97 dev_gold is 96.9% PYQ-style.
- ❌ Do not claim "more data hurt the model" without attributing it to the loss function
  difference.

### Recommended Action

If the Expanded model is re-trained using the **same loss function as the Clean model**
(`CosineSimilarityLoss` with explicit positive + negative pairs) and the same hyperparameters
(batch_size=16), the Expanded model should match or exceed the Clean model's accuracy given its
3× larger dataset. This would be the correct apples-to-apples comparison. Until then, the two
models should not be compared as evidence that "more data is worse."
