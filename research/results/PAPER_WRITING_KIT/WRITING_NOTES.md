# CampusClimb Paper Writing Notes & Methodological Limitations

This document outlines key writing guidelines, methodological constraints, and generalization limits that must be explicitly detailed in the final manuscript.

---

## 1. Disclosed Methodological Limitation: Loss-Function Mismatch

When discussing the contrastive learning framework in the **Methodology** or **Discussion** section, authors must address the choice of contrastive loss function and its impact on performance under low-resource constraints:

- **Finding**: We evaluated two fine-tuning configurations: **CosineSimilarityLoss** (reported Clean-97 model) and **MultipleNegativesRankingLoss** (exploratory Expanded-294 model). 
- **Performance Gap**: Despite having access to a larger training pool (294 samples), the MultipleNegativesRankingLoss model achieved lower forced Top-1 accuracy (**61.14%** vs. **64.63%** for CosineSimilarityLoss on 97 samples).
- **Explanation**: In low-data regimes (training size $n < 300$), CosineSimilarityLoss with explicit negative pairs outperforms MultipleNegativesRanking (MNR) loss. MNR relies on in-batch negatives, which typically require much larger batch sizes (e.g., 64–128+) than our training scale could support. This finding highlights a methodology boundary where standard contrastive loss choices can lead to sub-optimal results when training data is highly constrained.
- **Reference**: Detailed parameters and loss curves are recorded in [methodology_note_loss_function.md](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/methodology_note_loss_function.md).

---

## 2. Disclosed Generalization Limitation: LOSO Underperformance

When describing generalization, the manuscript must avoid framing CampusClimb as a broad, domain-agnostic algorithm. Instead, use the following guidelines:

- **Framing**: Frame the system strictly as a **"localized, subject-specific system"** rather than a "generalizable method".
- **Evidence**: Leave-One-Subject-Out (LOSO) cross-validation results show that zero-shot subject transfer yields an aggregate Top-1 accuracy of only **50.17%** (dropping to **41.05%** on Operating Systems), which is substantially lower than the in-domain baseline of **64.63%**.
- **Implication**: Curriculum vocabularies and structural contexts are highly disjoint across subjects (e.g., Operating Systems vs. Computer Networks vs. DBMS). Zero-shot cross-subject generalization is insufficient without localized fine-tuning. Future expansions must collect subject-specific training pairs rather than relying on cross-subject zero-shot inference.

---

## 3. Figure Verification Checklist

To ensure absolute visual and numerical integrity of the manuscript, verify that the generated figures in `FIGURES/` exactly match the data in the text and tables:

1. **Figure 1 (fig1_baseline_comparison_barchart.png)**:
   - Check that the height of each bar matches the Top-1 Accuracies in Table I (e.g., TF-IDF = 22.27%, FT SBERT = 62.88%, FT Hybrid = 64.63%).
   - Verify that the 95% Confidence Interval error bars match the ranges shown in Table I (e.g., FT Hybrid CI ends at 58.24% and 70.53%).
2. **Figure 2 (fig2_component_ablation_waterfall.png)**:
   - Verify the value labels on top of each ablation delta bar (Stage 2: -6.11pp, Stage 3: -4.37pp, Stage 4: 0.00pp, Stage 5: -5.68pp) match the Δ column in Table III.
3. **Figure 3 (fig3_loso_per_subject.png)**:
   - Ensure the bar heights for the subjects OS, CN, and DBMS correspond to 41.05%, 58.06%, and 51.39% respectively (Table II).
   - Ensure the horizontal line representing the in-domain FT Hybrid baseline is drawn exactly at 64.63%.
4. **Figure 4 (fig4_precision_recall_tradeoff.png)**:
   - Verify the coverage bar is at 91.70% and the accuracy-on-covered bar is at 67.14% (Table IV).
5. **Figure 5 (fig5_confusion_matrix_or_error_breakdown.png)**:
   - Verify that all three error category bars (Near-miss, Cross-subject, Ambiguous) are at exactly 6 samples each.
