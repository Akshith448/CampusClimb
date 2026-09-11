# Project Cleanup Audit and Proposal

This document outlines the proposed cleanup of the CampusClimb repository to streamline the codebase and present a professional, clean GitHub repository for the academic publication. 

> [!IMPORTANT]
> This audit does **NOT** modify or delete any file automatically. All recommendations are categorized by risk, checking for internal dependencies or references via project-wide grep searches and вчера's pre-writing audit checklist.

---

## 1. Deletion Candidates by Risk Level

### Category A: Safe to Delete
*These files are dead code, scratch scripts, or intermediate/superseded outputs that are completely isolated and not referenced or imported by any active pipeline or entry point.*

#### A.1 Root-Level Scripts & Backups
* `fine_tuned_capt_m (1).zip` (Root)
  - **Reason:** Large 405MB zip backup from local download. Unreferenced in project.
  - **Reference Check:** Grep search returned 0 results.
* `debug_evaluation.py` (Root)
  - **Reason:** Root-level testing/playground script for manual developer testing.
  - **Reference Check:** Grep search returned 0 results.
* `remap_existing.py` (Root)
  - **Reason:** Migration/remapping helper.
  - **Reference Check:** Grep search returned 0 results.

#### A.2 `evaluation/scratch/` Folder
* **All contents:**
  - `evaluation/scratch/analyse_pool.py`
  - `evaluation/scratch/analyse_pool2.py`
  - `evaluation/scratch/check_labels.py`
  - `evaluation/scratch/final_consolidation.py`
  - `evaluation/scratch/get_indomain_per_subject.py`
  - `evaluation/scratch/investigate_mcnemar.py`
  - `evaluation/scratch/run_clean_loso.py`
  - **Reason:** Playground scripts used by developers during data consolidation. Unreferenced in any active runner.
  - **Reference Check:** Grep search returned 0 results.

#### A.3 `evaluation/archive_old_88_sample_results/` Folder
* **All contents:**
  - `evaluation/archive_old_88_sample_results/ablation_results.csv`
  - `evaluation/archive_old_88_sample_results/dedup_results.txt`
  - `evaluation/archive_old_88_sample_results/efficiency_stats.txt`
  - `evaluation/archive_old_88_sample_results/failure_cases.csv`
  - `evaluation/archive_old_88_sample_results/gold_dedup_FINAL_LABELED.csv`
  - `evaluation/archive_old_88_sample_results/gold_mapping_EXPANDED.csv`
  - `evaluation/archive_old_88_sample_results/mapping_results.txt`
  - `evaluation/archive_old_88_sample_results/per_topic_breakdown.csv`
  - `evaluation/archive_old_88_sample_results/tfidf_mapping_results.txt`
  - **Reason:** Archive of results from an older 88-sample split evaluation. Superseded by the new authoritative 326 held-out test split.
  - **Reference Check:** Grep search returned 0 results.

#### A.4 Deprecated Diagnostic & One-Off Scripts (`evaluation/`)
* **List of files:**
  - `evaluation/archive_old_results.ps1`
  - `evaluation/audit_embedding_checksum.py`
  - `evaluation/check_db.py`
  - `evaluation/check_dbms_db.py`
  - `evaluation/check_dbms_mappings.py`
  - `evaluation/check_dbms_topics.py`
  - `evaluation/check_notes.py`
  - `evaluation/check_overlap_expanded.py`
  - `evaluation/debug_match.py`
  - `evaluation/inspect_all_topics.py`
  - `evaluation/inspect_ambiguous.py`
  - `evaluation/inspect_labels.py`
  - `evaluation/list_all_topics_full.py`
  - `evaluation/list_dbms_flagged.py`
  - `evaluation/list_os_flagged.py`
  - `evaluation/list_os_topics.py`
  - `evaluation/list_real_os_flagged.py`
  - `evaluation/list_remaining_flagged.py`
  - `evaluation/list_remaining_os_flagged.py`
  - `evaluation/list_zip.py`
  - `evaluation/search_topics_all.py`
  - `evaluation/view_flagged.py`
  - **Reason:** Utility diagnostics to list database counts, verify topics, or review specific flagging rules. They are not part of replication.
  - **Reference Check:** Unreferenced in active codebase.

#### A.5 Deprecated Pipeline Tasks (`evaluation/`)
* **List of files:**
  - `evaluation/task1_fix_dedup.py`
  - `evaluation/task2_expand_gold_mapping.py`
  - `evaluation/task3_per_topic_failures.py`
  - `evaluation/task4_remap_captm.py`
  - `evaluation/task6_efficiency.py`
  - **Reason:** One-off utility scripts written for specific developer sprint tasks.
  - **Reference Check:** Unreferenced in active codebase.

#### A.6 Experimental Pipeline Steps (`evaluation/`)
* **List of files:**
  - `evaluation/step1_dedup_threshold_sweep.py`
  - `evaluation/step2_error_analysis.py`
  - `evaluation/step3_hybrid_ensemble.py`
  - `evaluation/step3_hybrid_v2.py`
  - `evaluation/step4_final_ablation.py`
  - `evaluation/step5_check_leakage.py`
  - `evaluation/step5_fine_tune.py`
  - `evaluation/step5_fine_tune_production.py`
  - `evaluation/step5_fine_tune_production_clean.py`
  - `evaluation/step5_generate_training_pool.py`
  - `evaluation/step5_manual_label_flagged.py`
  - **Reason:** Scripts representing step-by-step developer experimentation on older model configurations. Consolidated into `run_academic_strengthening.py` and `run_full_evaluation.py`.
  - **Reference Check:** Only referenced in older pipeline step drafts.

#### A.7 Superseded Outputs & Datasets (`evaluation/output/`)
* **List of files:**
  - `evaluation/output/expanded_vs_clean_diagnostic_EXPANDED_MODEL_ARCHIVED.md`
  - `evaluation/output/reframed_abstract_intro_conclusion_EXPANDED_MODEL_ARCHIVED.md`
  - `evaluation/output/gold_mapping_EXPANDED_EXPANDED_MODEL_ARCHIVED.csv`
  - `evaluation/output/step5_production_results_DEPRECATED_EXPANDED_MODEL_ARCHIVED.txt`
  - `evaluation/output/step5_production_results_clean_DEPRECATED.txt`
  - `evaluation/output/step5_production_results_expanded_venv_DEPRECATED_EXPANDED_MODEL_ARCHIVED.txt`
  - `evaluation/output/fine_tuning_results.txt`
  - `evaluation/output/gold_mapping_250.csv`
  - `evaluation/output/gold_dedup_200.csv`
  - `evaluation/output/MASTER_RESULTS.csv`
  - `evaluation/output/ablation_results.csv` (Note: Invalid ablation results from the 326-pool)
  - `evaluation/output/ablation_results_testset_summary.txt`
  - **Reason:** Superseded datasets and intermediate outputs from older runs. Confirmed as obsolete and not cited in any paper draft.
  - **Reference Check:** Unreferenced in active codebase.

---

### Category B: Verify First
*These files are candidate cleanup targets, but removing them requires code modifications because they are currently written or read in active codebase scripts.*

* `evaluation/output/expanded_training_pool.csv`
  - **Why candidate:** Clean dev/test split mapping is now the gold standard.
  - **Reference Check:** **WARNING:** Read by `evaluation/run_academic_strengthening.py` on line 191 to fit baseline Logistic Regression classifiers. Deleting it will break that script.
* `evaluation/output/leave_one_subject_out.csv`
  - **Why candidate:** Result file generated by Colab GPU.
  - **Reference Check:** Read by `evaluation/run_academic_strengthening.py` on line 348 to load LOSO results. Deleting it will cause the script to skip the LOSO audit summary.
* `evaluation/output/extended_baseline_comparison.csv`, `capt_m_component_ablation.csv`, `significance_tests.csv`, `pairwise_confidence_intervals.csv`
  - **Why candidate:** Consolidated in `FINAL_authoritative_results.csv`.
  - **Reference Check:** Written by `run_academic_strengthening.py` and referenced in `REPRODUCIBILITY.md`.
* `evaluation/colab_finetune_expanded.py` & `evaluation/colab_loso_finetune.py`
  - **Why candidate:** References to external Google Colab GPU scripts. Not run locally.
  - **Reference Check:** Helpful for readers attempting GPU fine-tuning; verify if they should be placed in a `docs/` folder instead of evaluation code.

---

### Category C: Keep for Documentation / Developer Utility (Citations / Guides)
*These files are valuable guides, standard developer utilities, or results explicitly cited/needed in paper drafts (marked "✅ CITE").*

* **✅ CITE Result Files (Crucial for Paper Writing):**
  - `evaluation/output/abstention_metrics.csv`
  - `evaluation/output/baseline_comparison.csv`
  - `evaluation/output/baseline_comparison_summary.txt`
  - `evaluation/output/FINAL_headline_results.txt`
  - `evaluation/output/ablation_results_testset.csv` (Corrected held-out-test-set ablation results)
  - **Reason:** Retained specifically for direct citation and text verification in paper writing, as validated in the pre-writing audit.
* **Active Diagnostic Notes:**
  - `evaluation/output/EVALUATION_SUMMARY.md`: Master markdown index of results.
  - `evaluation/output/clean_vs_expanded_diagnostic.md`: Detailed discussion of contrastive loss mismatch.
  - `evaluation/output/error_analysis.md`: Detailed error breakdown on top-1 mismatches.
  - `evaluation/output/methodology_note_loss_function.md`: Technical description of embedding fine-tuning metrics.
  - `evaluation/output/pyq_importance_full_table.md` & `pyq_importance_percentile_table.md`: Rendered importance score tables.
  - `evaluation/output/cross_validation_summary.md` & `dedup_jaccard_summary.md`: Hyperparameter documentation.
* **Developer CLI Helpers:**
  - `evaluation/evaluate_dedup.py` & `evaluation/evaluate_mapping.py`: Standalone CLI accuracy calculators, referenced in `README.md`.
  - `evaluation/label_dedup_pairs.py`: Pair generation script, referenced in `README.md`.

---

## 2. Security Check: `.env` Exclusion
We have verified that the local environment configuration file is secure and will not leak:
* **`.gitignore` status:** Checked and confirmed. Line 16 of [.gitignore](file:///c:/Users/rahul/Downloads/CampusClimb/.gitignore) explicitly contains `.env`.
* **Git tracking status:** Run `git ls-files --error-unmatch .env` and confirmed that git returned `"error: pathspec '.env' did not match any file(s) known to git"`. This verifies `.env` is **untracked** and completely safe from accidental commits.

---

## 3. Proposed Clean Folder Structure

To present the project professionally on GitHub, we suggest organizing the repository into a clean layout:

```
CampusClimb/
├── app/                        # FastAPI Web application
│   ├── main.py                 # Backend entry point
│   ├── database.py             # SQLAlchemy engine & session configuration
│   ├── models.py               # MySQL ORM models
│   ├── routers/                # Endpoint route logic
│   │   ├── dashboard.py
│   │   └── upload.py
│   ├── static/                 # Web assets (CSS)
│   └── templates/              # Jinja2 template screens
│
├── core/                       # Core NLP Pipeline Modules
│   ├── pdf_extractor.py        # PDF extraction & layout chunker
│   ├── embeddings.py           # Semantic representation module
│   ├── topic_mapper.py         # Cosine NN + hybrid mapper
│   ├── deduplicator.py         # Cosine clusterer & Union-Find
│   ├── pyq_analyzer.py         # Question extractor & importance scorer
│   ├── note_formatter.py       # Study guide text builder
│   └── syllabus_parser.py      # Syllabus parser
│
├── evaluation/                 # Reproducibility evaluation pipeline
│   ├── run_full_evaluation.py  # Master evaluation script
│   ├── run_academic_strengthening.py # McNemar/Bootstrap significance script
│   ├── baseline_tfidf.py       # Baseline Lexical Model
│   ├── baseline_lda.py         # Baseline Topic Model
│   ├── evaluate_mapping.py     # Mapping accuracy evaluator
│   ├── evaluate_dedup.py       # Deduplication F1 evaluator
│   └── label_dedup_pairs.py    # Pair generator
│
├── evaluation/output/          # Authority datasets & reports
│   ├── gold_mapping_326.csv    # Gold mapping benchmark (229 test, 97 dev)
│   ├── dedup_manual_labeling.csv # Labeled duplicate pairs benchmark (90 pairs)
│   ├── FINAL_authoritative_results.csv # Consolidated performance table
│   ├── EVALUATION_SUMMARY.md   # Authority summary of paper results
│   ├── clean_vs_expanded_diagnostic.md # Technical diagnostics
│   └── error_analysis.md       # Qualitative error log
│   └── (CITED files: abstention_metrics.csv, baseline_comparison.csv, etc.)
│
├── docs/                       # Auxiliary documentation
│   └── colab/                  # Google Colab GPU training templates
│       ├── colab_finetune_expanded.py
│       └── colab_loso_finetune.py
│
├── uploads/                    # Git-ignored local file repository
├── config.py                   # System thresholds & global constants
├── requirements.txt            # Python dependencies configuration
├── README.md                   # Setup guide & framework summary
└── REPRODUCIBILITY.md          # Step-by-step academic validation checklist
```
