"""
RAG 2.0 Benchmark and Quality Evaluation Suite.

Evaluates:
1. Query understanding & pronoun resolution on conversational context
2. Hybrid BM25 + Dense RRF fusion ranking
3. Citation validation and hallucination stripping
4. Golden dataset mode accuracy (Notes vs General Knowledge)
5. Zero note context preservation in general fallback
"""

import json
import os
import sys
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.rag_engine import (
    compute_bm25_lexical_score,
    compute_lexical_overlap,
    evaluate_evidence,
    extract_keywords,
    get_localized_notice,
    resolve_conversational_query,
    validate_and_clean_citations,
)
from app.schemas import CitationItem


# ─────────────────────────────────────────────────────────────────────────────
# 1. Tests for Conversational Pronoun Resolution
# ─────────────────────────────────────────────────────────────────────────────

class TestConversationalUnderstanding:
    def test_resolves_pronoun_its(self):
        history = [
            {"role": "user", "content": "What is CPU scheduling in operating system?"},
            {"role": "assistant", "content": "CPU scheduling selects which ready process executes."},
        ]
        rewritten = resolve_conversational_query("What are its main advantages?", history)
        assert "cpu scheduling" in rewritten.lower()

    def test_resolves_starvation_query(self):
        history = [
            {"role": "user", "content": "Explain priority scheduling algorithm."},
            {"role": "assistant", "content": "Priority scheduling allocates CPU to highest priority process."},
        ]
        rewritten = resolve_conversational_query("How does it avoid starvation?", history)
        assert "priority scheduling" in rewritten.lower()

    def test_leaves_standalone_query_unmodified(self):
        standalone = "Explain deadlock and its four necessary conditions."
        rewritten = resolve_conversational_query(standalone, [])
        assert rewritten == standalone


# ─────────────────────────────────────────────────────────────────────────────
# 2. Tests for BM25 Lexical & Technical Acronym Matching
# ─────────────────────────────────────────────────────────────────────────────

class TestLexicalBM25Matching:
    def test_exact_acronym_match_boost(self):
        q_tokens = extract_keywords("What is PCB?")
        doc1_tokens = extract_keywords("A Process Control Block (PCB) is a data structure storing process state.")
        doc2_tokens = extract_keywords("General operating system memory structure and registers.")

        score1 = compute_bm25_lexical_score(q_tokens, doc1_tokens)
        score2 = compute_bm25_lexical_score(q_tokens, doc2_tokens)
        assert score1 > score2
        assert score1 > 0.0

    def test_lexical_overlap_hindi_hinglish(self):
        q = "CPU scheduling kya hai aur iske algorithms kaunse hain?"
        doc = "CPU scheduling algorithms include FCFS, SJF, and Round Robin."
        overlap = compute_lexical_overlap(q, doc)
        assert overlap >= 0.5


# ─────────────────────────────────────────────────────────────────────────────
# 3. Tests for Citation Validation & Hallucination Defense
# ─────────────────────────────────────────────────────────────────────────────

class TestCitationValidation:
    def test_strips_out_of_bounds_citations(self):
        citations = [
            CitationItem(citation_id=1, source_id=10, source_name="os1.pdf", chunk_id=101, snippet="Text 1"),
            CitationItem(citation_id=2, source_id=10, source_name="os1.pdf", chunk_id=102, snippet="Text 2"),
        ]
        raw_answer = "Process states include ready and running [1]. Also page replacement is used [99]."
        cleaned_ans, valid_cits = validate_and_clean_citations(raw_answer, citations)

        assert "[1]" in cleaned_ans
        assert "[99]" not in cleaned_ans  # Hallucinated citation stripped!
        assert len(valid_cits) == 2

    def test_empty_citations_strips_all_brackets(self):
        raw_answer = "Quantum computing uses qubits in superposition [1] [2]."
        cleaned_ans, valid_cits = validate_and_clean_citations(raw_answer, [])
        assert "[1]" not in cleaned_ans
        assert "[2]" not in cleaned_ans
        assert valid_cits == []


# ─────────────────────────────────────────────────────────────────────────────
# 4. Golden Dataset Evaluation
# ─────────────────────────────────────────────────────────────────────────────

class TestGoldenDatasetAccuracy:
    @classmethod
    def setup_class(cls):
        data_path = os.path.join(os.path.dirname(__file__), "data", "rag_eval.json")
        with open(data_path, "r", encoding="utf-8") as f:
            cls.eval_data = json.load(f)

    def test_unanswerable_questions_classified_as_not_found(self):
        unans = [q for q in self.eval_data if q["expected_mode"] == "NOTES_NOT_FOUND"]
        assert len(unans) >= 10

        for item in unans:
            # Synthetic OS candidate representing unrelated OS chunks
            candidates = [
                {
                    "chunk_id": 1,
                    "dense_score": 0.28,
                    "lexical_score": 0.0,
                    "chunk_text": "Processes are managed by the kernel and scheduled by CPU schedulers.",
                }
            ]
            mode, top_chunks, score, label = evaluate_evidence(
                query=item["query"],
                candidates=candidates,
                topic_mapping_score=0.15,
            )
            assert mode in ("NOTES_NOT_FOUND", "NOTES_WEAK"), f"Query '{item['query']}' should be general fallback"
            assert top_chunks == []
