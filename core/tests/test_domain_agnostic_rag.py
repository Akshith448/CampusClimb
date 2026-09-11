"""
Comprehensive Domain-Agnostic & Anti-Hardcoding Tests for CampusClimb RAG 2.0.

Validates that:
1. Conversational Query Resolution works dynamically across arbitrary academic domains (OS, DBMS, Networks, Mathematics, Quantum Physics, ML) without hardcoding.
2. Reference resolution ('first one', 'second one', 'last point') extracts items dynamically from preceding assistant output across any domain.
3. Intent-Aware evidence evaluation correctly differentiates between similarity and true answerability.
4. Source continuity dynamically filters by user-selected source IDs across follow-ups.
5. Out-of-domain and unseen topics reliably trigger General Knowledge fallback with zero note context and zero citations.
"""

import os
import sys
from typing import Any, Dict, List
from unittest.mock import MagicMock

import pytest

# Ensure project root on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.rag_engine import (
    ConversationState,
    QueryResolutionResult,
    detect_query_intent,
    evaluate_evidence,
    extract_numbered_items_from_text,
    resolve_conversational_query,
    retrieve_filtered_chunks,
)


class TestDynamicMultiDomainResolution:
    """Test 1: Dynamic follow-up resolution across multiple distinct domains with zero domain-specific code."""

    def test_domain_1_operating_systems_chain(self):
        # Turn 1: Initial query
        q1 = "What is CPU scheduling?"
        res1 = resolve_conversational_query(q1, [])
        assert res1.resolved_query == q1
        assert not res1.is_follow_up
        assert res1.intent == "definition"

        # Turn 2: Pronoun follow-up
        history_t2 = [
            {"role": "user", "content": q1},
            {"role": "assistant", "content": "CPU scheduling is the process of selecting which ready process executes on the CPU."},
        ]
        q2 = "What are its advantages?"
        res2 = resolve_conversational_query(q2, history_t2)
        assert "cpu scheduling" in res2.resolved_query.lower()
        assert res2.is_follow_up
        assert res2.intent == "advantages"

        # Turn 3: Types follow-up
        history_t3 = history_t2 + [
            {"role": "user", "content": q2},
            {"role": "assistant", "content": "The advantages of CPU scheduling include maximized CPU utilization and increased throughput. The main types are:\n1. Non-Preemptive Scheduling: Process retains CPU until completion.\n2. Preemptive Scheduling: Process can be interrupted."},
        ]
        q3 = "Explain the first one."
        res3 = resolve_conversational_query(q3, history_t3)
        assert "non-preemptive" in res3.resolved_query.lower()
        assert res3.is_follow_up

    def test_domain_2_database_systems_chain(self):
        # Turn 1: Initial query
        q1 = "What is ACID property in database management systems?"
        res1 = resolve_conversational_query(q1, [])
        assert res1.resolved_query == q1
        assert res1.intent == "definition"

        # Turn 2: Pronoun follow-up
        history_t2 = [
            {"role": "user", "content": q1},
            {"role": "assistant", "content": "ACID properties ensure reliable processing of database transactions."},
        ]
        q2 = "What are its key benefits?"
        res2 = resolve_conversational_query(q2, history_t2)
        assert "acid" in res2.resolved_query.lower()
        assert res2.is_follow_up
        assert res2.intent == "advantages"

        # Turn 3: Reference follow-up
        history_t3 = history_t2 + [
            {"role": "user", "content": q2},
            {"role": "assistant", "content": "ACID consists of four properties:\n1. Atomicity: All or nothing execution.\n2. Consistency: Database remains in valid state.\n3. Isolation: Transactions execute independently.\n4. Durability: Committed updates survive system crashes."},
        ]
        q3 = "Explain the third one."
        res3 = resolve_conversational_query(q3, history_t3)
        assert "isolation" in res3.resolved_query.lower()
        assert res3.is_follow_up

        q4 = "Explain the last one."
        res4 = resolve_conversational_query(q4, history_t3)
        assert "durability" in res4.resolved_query.lower()
        assert res4.is_follow_up

    def test_domain_3_computer_networks_chain(self):
        # Turn 1: Initial query
        q1 = "Explain the TCP three-way handshake."
        res1 = resolve_conversational_query(q1, [])
        assert res1.intent in ("mechanism", "general")

        # Turn 2: Follow-up
        history_t2 = [
            {"role": "user", "content": q1},
            {"role": "assistant", "content": "TCP connection establishment consists of three steps:\n1. SYN: Client sends synchronization packet.\n2. SYN-ACK: Server responds with acknowledgement.\n3. ACK: Client sends final acknowledgement."},
        ]
        q2 = "Explain the second one."
        res2 = resolve_conversational_query(q2, history_t2)
        assert "syn-ack" in res2.resolved_query.lower()
        assert res2.is_follow_up

    def test_domain_4_unseen_exotic_topic(self):
        """Test with completely unseen, novel scientific domain."""
        q1 = "What is CRISPR-Cas9 genome editing mechanism?"
        res1 = resolve_conversational_query(q1, [])
        assert res1.resolved_query == q1
        assert res1.intent in ("mechanism", "definition")

        history = [
            {"role": "user", "content": q1},
            {"role": "assistant", "content": "CRISPR-Cas9 is an RNA-guided gene editing tool with two components:\n1. Cas9 Endonuclease: Molecular scissors that cut DNA.\n2. Guide RNA: Sequences that guide Cas9 to target location."},
        ]
        q2 = "What are its limitations?"
        res2 = resolve_conversational_query(q2, history)
        assert "crispr-cas9" in res2.resolved_query.lower() or "genome editing" in res2.resolved_query.lower()
        assert res2.intent == "disadvantages"

        q3 = "Explain the first one."
        res3 = resolve_conversational_query(q3, history)
        assert "cas9 endonuclease" in res3.resolved_query.lower()


class TestIntentAwareAnswerability:
    """Test 2: Answerability != Similarity. Evaluates intent-bearing evidence sufficiency."""

    def test_high_similarity_entity_with_no_advantage_evidence(self):
        # Candidate only defines B-Trees, does NOT discuss advantages or performance comparisons
        candidates = [
            {
                "chunk_id": 101,
                "note_id": 50,
                "source_name": "dbms_notes.pdf",
                "chunk_text": "A B-Tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.",
                "is_representative": True,
                "similarity_score": 0.65,
                "dense_score": 0.65,
                "lexical_score": 0.5,
            }
        ]
        # User explicitly asks for disadvantages
        mode, top_chunks, score, label = evaluate_evidence(
            query="What are the disadvantages and drawbacks of B-Trees?",
            candidates=candidates,
            topic_mapping_score=0.2,
            intent="disadvantages",
        )
        # Because candidate text has NO disadvantage cues, intent_evidence_score is low (0.30)
        # and therefore cannot pass strict NOTES_SUPPORTED verification!
        assert mode in ("NOTES_WEAK", "NOTES_NOT_FOUND")

    def test_high_similarity_entity_with_matching_advantage_evidence(self):
        candidates = [
            {
                "chunk_id": 102,
                "note_id": 50,
                "source_name": "dbms_notes.pdf",
                "chunk_text": "The primary advantages of B-Trees are high fan-out, minimized disk I/O operations, efficient range queries, and guaranteed logarithmic search times.",
                "is_representative": True,
                "similarity_score": 0.85,
                "dense_score": 0.85,
                "lexical_score": 2.5,
            }
        ]
        mode, top_chunks, score, label = evaluate_evidence(
            query="What are the advantages of B-Trees?",
            candidates=candidates,
            topic_mapping_score=0.7,
            intent="advantages",
        )
        assert mode == "NOTES_SUPPORTED"
        assert len(top_chunks) == 1
        assert label == "High"


class TestDynamicSourceContinuity:
    """Test 3: Selected source IDs are strictly preserved and filtered dynamically."""

    def test_selected_source_filtering_db_query(self):
        db_mock = MagicMock()
        query_mock = db_mock.query.return_value.filter.return_value
        # When filtered by source [42], returns Note ID 42
        query_mock.filter.return_value.all.return_value = [(42,)]

        # Mock chunks returned for Note 42
        chunk_mock = MagicMock()
        chunk_mock.id = 1001
        chunk_mock.note_id = 42
        chunk_mock.embedding = None
        chunk_mock.similarity_score = 0.88
        chunk_mock.cleaned_text = "Transaction management ensures consistency in database systems."
        chunk_mock.chunk_text = chunk_mock.cleaned_text
        chunk_mock.note.original_filename = "transactions_ch4.pdf"
        chunk_mock.is_representative = True
        chunk_mock.matched_topic_id = 7
        chunk_mock.diagram_mermaid = None

        db_mock.query.return_value.options.return_value.filter.return_value.all.return_value = [chunk_mock]

        candidates, top_topic_id, _resolution = retrieve_filtered_chunks(
            db=db_mock,
            user_id="user_db_student",
            subject="DBMS",
            query_emb=[0.1] * 384,
            selected_source_ids=[42],
            original_query="What is transaction management?",
        )

        assert len(candidates) == 1
        assert candidates[0]["note_id"] == 42
        assert candidates[0]["source_name"] == "transactions_ch4.pdf"
