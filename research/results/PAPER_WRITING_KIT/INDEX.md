# CampusClimb Paper Writing Reference Kit – Index

This kit consolidates all required assets, tables, figures, and textual revisions necessary to write the CampusClimb IEEE paper. All figures and numbers are strictly sourced from the verified Clean-97 model (`MASTER_RESULTS.csv`).

## Kit Contents

1. **[INDEX.md](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/INDEX.md)**: This file, detailing the layout and purpose of the writing kit.
2. **[RESULTS_TABLES.md](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/RESULTS_TABLES.md)**: Standardized, copy-pasteable IEEE tables containing:
   - Table I: Baseline Comparison
   - Table II: LOSO Generalization
   - Table III: Component Ablation Study
   - Table IV: Gated Abstention-Aware Metrics
   - Table V: McNemar Significance Tests
   - Table VI: Paired Bootstrap Confidence Intervals
3. **[KEY_NUMBERS_CHEATSHEET.md](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/KEY_NUMBERS_CHEATSHEET.md)**: A quick-reference summary of the headline metrics, test results, and bootstrap intervals for rapid validation during drafting.
4. **[WRITING_NOTES.md](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/WRITING_NOTES.md)**: Crucial documentation detailing constraints, figure verification processes, and authoring guidelines.
5. **[reframed_abstract_intro_conclusion.md](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/reframed_abstract_intro_conclusion.md)**: IEEE-ready draft revisions for the Abstract, Introduction closing, and Conclusion opening, with proper framing of:
   - Generalization limitation: LOSO underperformance (system framed as a *localized, subject-specific system*, not a *generalizable method*).
   - Methodological limitation: Loss-function mismatch under low-data constraints (CosineSimilarityLoss vs. MultipleNegativesRankingLoss).
6. **[generate_figures.py](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/generate_figures.py)**: The Python plotting script that reads directly from `MASTER_RESULTS.csv` and outputs 300 DPI publication-ready figures.
7. **[FIGURES/](file:///c:/Users/rahul/Downloads/CampusClimb/evaluation/output/PAPER_WRITING_KIT/FIGURES/)**: Folder containing the five generated high-resolution PNG plots:
   - `fig1_baseline_comparison_barchart.png`
   - `fig2_component_ablation_waterfall.png`
   - `fig3_loso_per_subject.png`
   - `fig4_precision_recall_tradeoff.png`
   - `fig5_confusion_matrix_or_error_breakdown.png`
