# CampusClimb: Reframed Academic Text (Abstract, Introduction, and Conclusion)

This document contains the reframed publication draft text for the Abstract, Introduction closing, and Conclusion opening paragraphs of the CampusClimb paper, using the reconciled Clean-97 model results.

---

## 1. Revised Abstract

University course syllabi provide a critical roadmap for students, yet aligning heterogeneous learning materials (e.g., student-written lecture notes or slides) with formal syllabus topics remains a challenging, manual task. In this work, we address the problem of **localized academic topic mapping under limited in-domain data**—a setting common in single-university or course-specific environments. We present CampusClimb, an applied educational NLP system that maps unstructured note chunks to fine-grained syllabus topics. Since curriculum structures and academic vocabularies vary widely across subjects, general-purpose zero-shot models often struggle. To overcome this, we employ a localized contrastive fine-tuning approach using a small pool of course-specific syllabus-to-note mappings. We evaluate our approach on a strictly disjoint held-out test split (229 samples) with zero train/test leakage.

Our fine-tuned Clean-97 Hybrid model achieves a **64.63% Top-1 accuracy** under force-mapping, a **82.97% Top-3 accuracy**, and a **0.5482 Macro F1 score**, representing a statistically significant improvement ($p < 0.001$) over three strong baselines: a lexical TF-IDF+Logistic-Regression classifier (22.27% Top-1), an off-the-shelf sentence transformer model (all-MiniLM-L6-v2, 51.97% Top-1), and the base SBERT domain model (52.84% Top-1). When confidence-based abstention gating is enabled, our model achieves a raw overall accuracy of **61.57%** with **91.70% coverage** and **67.14% accuracy-on-covered**. Our findings demonstrate that localized semantic tuning is a highly effective, low-data method for subject-specific curriculum alignment.

---

## 2. Revised Introduction Closing Paragraph

Unlike broad-domain semantic search systems, this work focuses on a **localized, subject-specific system** rather than a generalizable method. We target deployments where a curriculum remains fixed over multiple academic semesters, and note-to-topic mapping must be highly precise to guide students effectively. We establish a rigorous evaluation framework using a disjoint held-out test split of 229 samples with strict leakage controls. Through this, we demonstrate that a localized, fine-tuned hybrid ensemble achieves statistically significant accuracy gains over lexical baselines, off-the-shelf sentence embeddings, and base domain sentence transformers ($p < 0.001$ for all primary baseline comparisons). 

As a scoping decision, the system is designed and validated for subject-specific deployment within a fixed curriculum. We explicitly test and report the limits of zero-shot subject transfer via leave-one-subject-out (LOSO) cross-validation, finding that transfer performance (**50.17% aggregate Top-1 accuracy**) underperforms the in-domain baseline, highlighting the difficulty of generalizability across disparate course content. Consequently, we frame our contribution as a localized applied educational system, leaving cross-subject zero-shot transfer as future work requiring subject-specific fine-tuning data.

---

## 3. Revised Conclusion Opening Paragraph

In this paper, we presented and evaluated a localized academic topic mapping system for university course curricula. By framing the task within a localized course deployment under limited in-domain data, we addressed the limitations of lexical models and base embedding models in capturing course-specific semantics. On a disjoint, stratified 229-sample test set, the fine-tuned Clean-97 Hybrid model achieved a Top-1 accuracy of **64.63%** (raw, forced) and **61.57%** (gated, with **67.14% accuracy-on-covered** and **91.70% coverage**), representing a highly significant statistical boost ($p < 0.001$) over TF-IDF+LR, off-the-shelf MiniLM, and base SBERT models. 

Our evaluations also highlighted key boundaries and limitations of our approach. First, cross-subject zero-shot generalization (LOSO) is insufficient, yielding only **50.17% aggregate Top-1 accuracy** (with individual subjects dropping as low as 41.05% for Operating Systems). This confirms that curriculum vocabularies across subjects (e.g., Operating Systems, DBMS, and Computer Networks) are highly disjoint, and that localized fine-tuning is required to establish reliable semantic alignments. Second, we observed a methodological limitation regarding the contrastive loss function: at our limited training scale (n = 97 pairs), using CosineSimilarityLoss with explicit negative pairs significantly outperformed MultipleNegativesRankingLoss, which suffers from in-batch negative constraints in low-resource regimes. This scoping positions CampusClimb as an effective localized applied educational tool, while outlining a clear roadmap for subject-specific data acquisition in future expansion efforts.
