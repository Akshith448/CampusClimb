"""
CampusClimb — Global Configuration

Tunable parameters for NLP processing, chunking, and importance scoring.
Adjust these values for experimentation (paper's Results section).
"""

import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check for fine-tuned CAPT-M model checkpoint
FINE_TUNED_MODEL_PATH = os.path.join(BASE_DIR, "research", "models", "fine_tuned_capt_m_clean")
EVAL_FINE_TUNED_PATH = os.path.join(BASE_DIR, "evaluation", "fine_tuned_capt_m_clean")

if os.path.isdir(FINE_TUNED_MODEL_PATH):
    MODEL_NAME = FINE_TUNED_MODEL_PATH
elif os.path.isdir(EVAL_FINE_TUNED_PATH):
    MODEL_NAME = EVAL_FINE_TUNED_PATH
else:
    logging.warning(
        "[CONFIG WARNING] Fine-tuned model checkpoint not found at '%s'. "
        "Falling back to baseline model 'all-MiniLM-L6-v2'.",
        FINE_TUNED_MODEL_PATH
    )
    MODEL_NAME = "all-MiniLM-L6-v2"

# Text chunking 
SENTENCES_PER_CHUNK = 4
MIN_CHUNK_WORDS = 20 

# Semantic deduplication 
DEDUP_SIMILARITY_THRESHOLD = 0.85

# Topic importance scoring thresholds
IMPORTANCE_LOW_THRESHOLD = 0.05
IMPORTANCE_HIGH_THRESHOLD = 0.15
