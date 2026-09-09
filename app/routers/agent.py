"""
Bilingual AI Agent Router — Multilingual Q&A & Explanation API (/api/v1/agent/).

Integrates CAPT-M semantic retrieval with external LLM API translation and
explanation generation, protected by rate limiting.
"""

import json
import os
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.auth import get_current_user
from app.database import get_db
from app.models import SyllabusTopic, NoteChunk
from app.rate_limiter import ai_rate_limiter
from app.schemas import AgentQueryRequest, AgentQueryResponse, SourceChunkSchema
from core.embeddings import get_embedding
from core.topic_mapper import map_chunks_batch_top2

load_dotenv()

router = APIRouter(prefix="/api/v1/agent", tags=["Bilingual Agent"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def _generate_llm_explanation(
    query: str,
    topic_name: str,
    context_chunks: List[str],
    target_language: str,
) -> tuple[str, str]:
    """Call external Gemini LLM REST API for translation and explanation.

    Returns tuple of (answer_text, explanation_text) translated into target_language.
    """
    if not GEMINI_API_KEY:
        # Fallback explanation if API key is not configured
        fallback_answer = f"[{target_language}] Answer for '{query}' based on topic '{topic_name}'."
        fallback_expl = f"[{target_language}] Detailed concepts for {topic_name}: " + " ".join(context_chunks[:2])
        return fallback_answer, fallback_expl

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""You are a bilingual academic tutor for university students studying {topic_name}.
Context from student notes:
{" --- ".join(context_chunks[:3])}

Question: {query}
Target Language: {target_language}

Instructions:
1. Provide a direct, clear answer to the question strictly in {target_language}.
2. Provide a brief 2-3 sentence concept explanation strictly in {target_language}.
Format response as JSON with keys "answer" and "explanation".
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }

    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=12)
        if res.status_code == 200:
            data = res.json()
            text_content = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(text_content)
            return parsed.get("answer", ""), parsed.get("explanation", "")
    except Exception:
        pass

    # Fallback formatting if Gemini call fails
    answer = f"Regarding '{query}' under '{topic_name}': " + (context_chunks[0] if context_chunks else topic_name)
    explanation = f"Explanation in {target_language}: Key study concept extracted for {topic_name}."
    return answer, explanation


@router.post("/query", response_model=AgentQueryResponse)
async def agent_query(
    request: Request,
    body: AgentQueryRequest,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    """Bilingual Agent endpoint — authenticated, rate limited, semantic retrieval."""
    # Enforce AI route rate limiting per IP
    ai_rate_limiter.check(request)

    # 1. Fetch syllabus topics for subject (or all subjects fallback)
    topics = db.query(SyllabusTopic).filter(SyllabusTopic.subject == body.subject).all()
    if not topics:
        topics = db.query(SyllabusTopic).all()

    if not topics:
        # If database is completely empty of syllabus topics
        return AgentQueryResponse(
            query=body.query,
            subject=body.subject,
            language=body.language,
            matched_topic="General Concept",
            confidence_score=0.0,
            confidence_label="Unmapped",
            answer=f"[{body.language}] Answer for '{body.query}'. (Note: Please upload a syllabus for {body.subject} to enable topic-specific matching).",
            explanation=f"[{body.language}] System is currently operating in general query mode because no syllabus has been uploaded yet.",
            sources=[],
        )

    # 2. Embed query and map to syllabus topics
    query_emb = get_embedding(body.query)
    topic_embeddings = [(t.id, json.loads(t.embedding)) for t in topics if t.embedding]
    topic_name_map = {t.id: t.topic_name for t in topics}

    mapping_results = map_chunks_batch_top2(
        [query_emb],
        topic_embeddings,
        chunk_texts=[body.query],
        topic_names=topic_name_map,
    )

    if not mapping_results:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to map query to topic space.",
        )

    top_mapping = mapping_results[0]
    matched_topic_id = top_mapping["top1_topic_id"]
    matched_topic_name = topic_name_map.get(matched_topic_id, "General Concept")

    # 3. Retrieve relevant note chunks mapped to this topic
    chunks = db.query(NoteChunk).filter(
        NoteChunk.matched_topic_id == matched_topic_id,
        NoteChunk.chunk_type.in_(["content", "table", None]),
    ).limit(5).all()

    context_texts = [c.chunk_text for c in chunks] if chunks else [matched_topic_name]

    sources = [
        SourceChunkSchema(
            id=c.id,
            text=c.chunk_text[:250] + ("..." if len(c.chunk_text) > 250 else ""),
            similarity_score=c.similarity_score,
        )
        for c in chunks
    ]

    # 4. Generate answer and explanation in target language
    answer, explanation = _generate_llm_explanation(
        query=body.query,
        topic_name=matched_topic_name,
        context_chunks=context_texts,
        target_language=body.language,
    )

    return AgentQueryResponse(
        query=body.query,
        subject=body.subject,
        language=body.language,
        matched_topic=matched_topic_name,
        confidence_score=top_mapping["top1_score"],
        confidence_label=top_mapping["confidence"],
        answer=answer,
        explanation=explanation,
        sources=sources,
    )
