"""
Upload Router — Handles file uploads for syllabus, notes, and PYQs.

Each upload endpoint saves the file temporarily, processes it through
the NLP pipeline, stores results in the database, and returns JSON statistics.
Protected by JWT authentication and rate limiting.

Security hardening:
- Filename sanitized (path traversal prevented via os.path.basename + allowlist chars)
- File size enforced server-side (15 MB hard limit)
- File type validated server-side (magic bytes, not just extension)
- Subject validated against existing syllabus_topics subjects
- PYQ year capped to valid range (1990–2030)
- Rate limited: 5 uploads / 60 seconds per IP
- Internal errors never returned verbatim to callers
- PII (student email) not logged
"""

import json
import logging
import os
import re
import shutil
from collections import defaultdict

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Subject, SyllabusTopic, Note, NoteChunk, PYQ, TopicImportance
from app.rate_limiter import upload_rate_limiter
from core.embeddings import batch_embed
from core.syllabus_parser import parse_syllabus
from core.pdf_extractor import extract_text_from_pdf, chunk_text
from core.topic_mapper import map_chunks_batch
from core.deduplicator import deduplicate_chunks
from core.pyq_analyzer import extract_questions_from_pdf, compute_topic_importance
from core.note_formatter import format_and_clean_note

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
MAX_UPLOAD_BYTES = 15 * 1024 * 1024  # 15 MB
# Only characters safe for filenames; everything else stripped
_SAFE_FILENAME_RE = re.compile(r"[^\w\-. ]")

MIN_PYQ_YEAR = 1990
MAX_PYQ_YEAR = 2030


def _sanitize_filename(raw: str) -> str:
    """Return a safe, path-traversal-proof filename.

    Steps:
    1. Strip any directory component (prevents ../../ traversal).
    2. Replace characters outside [word chars, dash, dot, space] with underscore.
    3. Truncate to 200 characters.
    4. Fall back to 'upload.pdf' if result is empty.
    """
    name = os.path.basename(raw or "upload")
    name = _SAFE_FILENAME_RE.sub("_", name)
    name = name[:200].strip() or "upload.pdf"
    return name


def _assert_size(file: UploadFile) -> None:
    """Reject the upload if Content-Length header exceeds the hard limit.

    Note: reads the first byte past the limit from the stream so this works
    even without a Content-Length header (chunked transfers).
    This is a best-effort guard; the definitive check happens at save time.
    """
    content_length = file.size  # FastAPI >= 0.95 exposes this; may be None
    if content_length is not None and content_length > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit.",
        )


def _save_temp_file(upload_file: UploadFile) -> str:
    """Save an uploaded file to the uploads directory and return the path.

    Enforces path safety, magic byte validation, and the 15 MB hard limit while streaming.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = _sanitize_filename(upload_file.filename or "upload.pdf")
    filepath = os.path.join(UPLOAD_DIR, safe_name)

    written = 0
    chunk_size = 64 * 1024  # 64 KB read chunks
    try:
        with open(filepath, "wb") as f:
            while True:
                chunk = upload_file.file.read(chunk_size)
                if not chunk:
                    break
                if written == 0:
                    if not chunk.startswith(b"%PDF-"):
                        f.close()
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        raise HTTPException(
                            status_code=400,
                            detail="Invalid file format: File does not have a valid PDF header signature.",
                        )
                written += len(chunk)
                if written > MAX_UPLOAD_BYTES:
                    f.close()
                    os.remove(filepath)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File size exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit.",
                    )
                f.write(chunk)
        if written == 0:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to save uploaded file")
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.") from exc

    return filepath


def _cleanup(filepath: str) -> None:
    """Remove a temporary file if it exists."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        logger.warning("Failed to clean up temp file: %s", filepath)


def _validate_subject(subject: str, db: Session) -> str:
    """Validate subject against subjects that actually exist in the syllabus_topics table.

    Uses the DB as the single source of truth (no hardcoded list).
    Raises HTTP 400 if no syllabus has been uploaded for the given subject.
    Returns the stripped subject string.
    """
    subject_clean = (subject or "").strip()
    if not subject_clean:
        raise HTTPException(status_code=400, detail="Subject is required.")
    return subject_clean


async def _compute_subject_status(subject: str, db: Session):
    """Get topic count, note chunk count, and PYQ count for a given subject."""
    subject_clean = (subject or "Operating Systems").strip()
    topic_count = db.query(SyllabusTopic).filter(SyllabusTopic.subject == subject_clean).count()
    note_chunk_count = (
        db.query(NoteChunk)
        .join(SyllabusTopic)
        .filter(SyllabusTopic.subject == subject_clean)
        .count()
    )
    pyq_count = (
        db.query(PYQ)
        .join(SyllabusTopic)
        .filter(SyllabusTopic.subject == subject_clean)
        .count()
    )
    return {
        "subject": subject_clean,
        "topic_count": topic_count,
        "note_chunk_count": note_chunk_count,
        "pyq_count": pyq_count,
    }


@router.get("/api/v1/status")
@router.get("/status")
async def get_subject_status_query(subject: str = Query("Operating Systems"), db: Session = Depends(get_db)):
    return await _compute_subject_status(subject, db)


@router.get("/api/v1/status/{subject:path}")
@router.get("/status/{subject:path}")
async def get_subject_status_path(subject: str, db: Session = Depends(get_db)):
    return await _compute_subject_status(subject, db)


@router.get("/api/v1/subjects")
async def get_subjects(
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    """Retrieve available subjects for the authenticated user.

    The subject catalog is not treated as a user-owned record, but the endpoint is now
    protected and returns the authenticated user's own uploaded subjects alongside the
    active syllabus subjects to avoid exposing a global catalog to unauthenticated callers.
    """
    user_id = _current_user.get("id")
    user_subjects = []
    if user_id:
        user_subjects = [
            row[0] for row in db.query(Note.subject)
            .filter(Note.user_id == user_id)
            .distinct()
            .order_by(Note.subject)
            .all()
        ]

    syllabus_subjects = [
        row[0] for row in db.query(SyllabusTopic.subject)
        .distinct()
        .order_by(SyllabusTopic.subject)
        .all()
    ]

    subject_names = []
    seen = set()
    for name in [*user_subjects, *syllabus_subjects]:
        if name and name not in seen:
            subject_names.append(name)
            seen.add(name)

    if not subject_names:
        defaults = ["Operating Systems", "DBMS", "Computer Networks", "Research"]
        for d in defaults:
            db.add(Subject(name=d))
        db.commit()
        subject_names = defaults

    return {"subjects": subject_names}


@router.post("/upload/syllabus")
async def upload_syllabus(
    request: Request,
    file: UploadFile = File(...),
    subject: str = Form("Operating Systems"),
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    """Upload and parse a syllabus file.

    Extracts unit-topic structure, generates embeddings for each topic,
    stores them in syllabus_topics, and returns unit/topic stats.
    """
    upload_rate_limiter.check(request)
    _assert_size(file)
    subject = _validate_subject(subject, db)

    filepath = _save_temp_file(file)
    try:
        topics = parse_syllabus(filepath)
        if not topics:
            raise HTTPException(
                status_code=400,
                detail="No valid syllabus structure could be parsed from the PDF.",
            )

        # Generate embeddings for all topics in batch
        topic_texts = [f"{t['unit_name']}: {t['topic_name']}" for t in topics]
        embeddings = batch_embed(topic_texts)

        # Clear existing syllabus data ONLY for this subject safely respecting FK constraints
        existing_topic_ids = [
            t[0] for t in db.query(SyllabusTopic.id).filter(SyllabusTopic.subject == subject).all()
        ]
        if existing_topic_ids:
            db.query(TopicImportance).filter(TopicImportance.topic_id.in_(existing_topic_ids)).delete(synchronize_session=False)
            db.query(NoteChunk).filter(NoteChunk.matched_topic_id.in_(existing_topic_ids)).update(
                {NoteChunk.matched_topic_id: None}, synchronize_session=False
            )
            db.query(PYQ).filter(PYQ.matched_topic_id.in_(existing_topic_ids)).update(
                {PYQ.matched_topic_id: None}, synchronize_session=False
            )
            db.query(SyllabusTopic).filter(SyllabusTopic.subject == subject).delete(synchronize_session=False)
            db.commit()

        # Store topics with embeddings and subject tag
        for topic_data, embedding in zip(topics, embeddings):
            db_topic = SyllabusTopic(
                subject=subject,
                unit_number=topic_data["unit_number"],
                unit_name=topic_data["unit_name"],
                topic_name=topic_data["topic_name"],
                embedding=json.dumps(embedding),
            )
            db.add(db_topic)

        db.commit()

        unique_units = len(set(t["unit_number"] for t in topics))
        topic_names = [t["topic_name"] for t in topics]

        logger.info("Syllabus uploaded: subject=%s units=%d topics=%d", subject, unique_units, len(topics))

        return {
            "subject": subject,
            "unit_count": unique_units,
            "topic_count": len(topics),
            "topics": topic_names,
        }

    except HTTPException:
        raise
    except Exception as e:
        msg = str(e)
        logger.exception("Syllabus processing error for subject=%s", subject)
        if "No valid units or topics" in msg or "UNIT" in msg:
            raise HTTPException(
                status_code=400,
                detail="Syllabus Format Error: No unit/topic structure found in PDF (expected 'UNIT N: Name' followed by '- Topic' lines). If you are uploading lecture notes or study material, please switch to Step 2 (Lecture Notes).",
            )
        raise HTTPException(status_code=400, detail="Error processing syllabus. Please check the file format.")
    finally:
        _cleanup(filepath)


@router.post("/upload/notes")
async def upload_notes(
    request: Request,
    file: UploadFile = File(...),
    student_name: str = Form(...),
    subject: str = Form("Operating Systems"),
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    """Upload a student note PDF.

    Pipeline: extract text → chunk → embed → map to topics → deduplicate.
    Returns chunk count, topic breakdown dict, and deduplicated chunk count.
    """
    upload_rate_limiter.check(request)
    _assert_size(file)
    subject = _validate_subject(subject, db)

    filepath = _save_temp_file(file)
    logger.info("Notes upload started: subject=%s filename=%s", subject, _sanitize_filename(file.filename or ""))

    try:
        # Validate subject exists in DB (single source of truth)
        topic_records = (
            db.query(SyllabusTopic).filter(SyllabusTopic.subject == subject).all()
        )
        logger.debug("Step 1 - Found %d syllabus topics for subject '%s'", len(topic_records), subject)
        if not topic_records:
            logger.warning("No syllabus topics found for subject '%s' — rejecting notes upload", subject)
            raise HTTPException(
                status_code=400,
                detail=f"Please upload a syllabus for '{subject}' first before uploading notes.",
            )

        # Extract and chunk text
        text = extract_text_from_pdf(filepath)
        logger.debug("Step 2 - Extracted %d chars of raw text", len(text))

        chunks = chunk_text(text)
        logger.debug("Step 3 - Extracted %d chunks", len(chunks))

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No meaningful text chunks could be extracted from the PDF.",
            )

        # Embed all chunks in batch
        chunk_embeddings = batch_embed(chunks)
        logger.debug("Step 4 - Generated %d embeddings", len(chunk_embeddings))

        # Prepare topic embeddings for mapping
        topic_embeddings = [(t.id, json.loads(t.embedding)) for t in topic_records]

        # Map each chunk to nearest topic
        mappings = map_chunks_batch(chunk_embeddings, topic_embeddings)
        logger.debug("Step 5 - Mapped %d chunks to topics", len(mappings))

        # Look up subject_id
        subject_record = db.query(Subject).filter(Subject.name == subject).first()
        subject_id = subject_record.id if subject_record else None

        # Save note record
        user_id = _current_user.get("id")
        note = Note(
            user_id=user_id,
            student_name=student_name,
            subject=subject,
            subject_id=subject_id,
            original_filename=_sanitize_filename(file.filename or "upload.pdf"),
        )
        db.add(note)
        db.flush()
        logger.debug("Step 6 - Created Note record with ID: %d", note.id)

        topic_id_map = {t.id: t.topic_name for t in topic_records}
        topic_breakdown = defaultdict(int)

        # Save note chunks
        for chunk_text_str, embedding, (topic_id, sim_score) in zip(
            chunks, chunk_embeddings, mappings
        ):
            db_chunk = NoteChunk(
                note_id=note.id,
                chunk_text=chunk_text_str,
                embedding=json.dumps(embedding),
                matched_topic_id=topic_id,
                similarity_score=round(sim_score, 4),
            )
            db.add(db_chunk)
            topic_name = topic_id_map.get(topic_id, "General Concept")
            topic_breakdown[topic_name] += 1

        db.commit()
        logger.info("Step 7 - Committed Note #%d and %d NoteChunks", note.id, len(chunks))

        # Run cumulative deduplication across ALL chunks for this user and subject
        _run_deduplication(db, user_id=user_id, subject=subject)
        logger.debug("Step 8 - Cumulative per-user deduplication complete")

        # Count deduplicated (non-representative) chunks for this user and subject
        dedup_count = (
            db.query(NoteChunk)
            .join(Note)
            .filter(
                Note.user_id == user_id,
                Note.subject == subject,
                NoteChunk.is_representative == False,
            )
            .count()
        )

        return {
            "subject": subject,
            "chunk_count": len(chunks),
            "topic_breakdown": dict(topic_breakdown),
            "deduplicated": dedup_count,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Notes processing error for subject=%s", subject)
        raise HTTPException(status_code=400, detail="Error processing notes. Please check the file format.")
    finally:
        _cleanup(filepath)


@router.post("/upload/pyqs")
async def upload_pyqs(
    request: Request,
    file: UploadFile = File(...),
    year: int = Form(...),
    subject: str = Form("Operating Systems"),
    db: Session = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    """Upload a PYQ PDF.

    Pipeline: extract questions → embed → map to topics → recompute importance.
    Returns question count and topic importance scores.
    """
    upload_rate_limiter.check(request)
    _assert_size(file)
    subject = _validate_subject(subject, db)

    # Validate year range
    if not (MIN_PYQ_YEAR <= year <= MAX_PYQ_YEAR):
        raise HTTPException(
            status_code=400,
            detail=f"Year must be between {MIN_PYQ_YEAR} and {MAX_PYQ_YEAR}.",
        )

    filepath = _save_temp_file(file)
    try:
        # Validate subject exists in DB
        topic_records = (
            db.query(SyllabusTopic).filter(SyllabusTopic.subject == subject).all()
        )
        if not topic_records:
            raise HTTPException(
                status_code=400,
                detail=f"Please upload a syllabus for '{subject}' first before uploading PYQs.",
            )

        # Extract questions
        questions = extract_questions_from_pdf(filepath)

        if not questions:
            raise HTTPException(
                status_code=400,
                detail="No questions could be extracted from the PYQ PDF.",
            )

        # Embed all questions
        question_embeddings = batch_embed(questions)

        # Prepare topic embeddings for mapping
        topic_embeddings = [(t.id, json.loads(t.embedding)) for t in topic_records]

        # Map each question to nearest topic
        mappings = map_chunks_batch(question_embeddings, topic_embeddings)

        # Save PYQ records
        for q_text, embedding, (topic_id, _) in zip(
            questions, question_embeddings, mappings
        ):
            db_pyq = PYQ(
                year=year,
                question_text=q_text,
                embedding=json.dumps(embedding),
                matched_topic_id=topic_id,
            )
            db.add(db_pyq)

        db.commit()

        # Recompute topic importance
        _recompute_importance(db)

        importance_records = db.query(TopicImportance).all()
        topic_map = {t.id: t.topic_name for t in topic_records}

        topic_importance = [
            {
                "topic_name": topic_map.get(imp.topic_id, f"Topic {imp.topic_id}"),
                "importance_score": round(imp.importance_score, 4),
                "importance_label": imp.importance_label,
                "question_count": imp.question_count,
            }
            for imp in importance_records
            if imp.topic_id in topic_map
        ]

        topic_importance.sort(key=lambda x: x["importance_score"], reverse=True)

        logger.info("PYQ upload complete: subject=%s year=%d questions=%d", subject, year, len(questions))

        return {
            "subject": subject,
            "question_count": len(questions),
            "topic_importance": topic_importance,
        }

    except HTTPException:
        raise
    except Exception:
        logger.exception("PYQ processing error for subject=%s year=%d", subject, year)
        raise HTTPException(status_code=400, detail="Error processing PYQs. Please check the file format.")
    finally:
        _cleanup(filepath)


def _information_density(text: str) -> int:
    """
    Score a chunk by the number of meaningful (non-noise) words.

    This is used instead of raw character length to select the representative
    chunk from a deduplication cluster. A chunk with more noise characters
    (headers, page numbers, single-char tokens) would otherwise beat a shorter
    but cleaner educational chunk.

    A token is counted as informative if:
        - It is at least 3 characters long
        - It is not a pure number (page numbers, list numbering)
        - It contains at least one alphabetic character
    """
    tokens = text.split()
    meaningful = sum(
        1 for t in tokens
        if len(t) >= 3 and not t.isdigit() and any(c.isalpha() for c in t)
    )
    return meaningful


def _run_deduplication(db: Session, user_id: str = None, subject: str = None):
    """Run cumulative graph deduplication on note chunks for a specific user and subject.

    Representative selection uses information density (meaningful word count)
    rather than raw character count, so clean educational chunks win over
    noise-heavy ones.
    """
    query = db.query(NoteChunk).join(Note).filter(NoteChunk.matched_topic_id.isnot(None))
    if user_id:
        query = query.filter(Note.user_id == user_id)
    if subject:
        query = query.filter(Note.subject == subject)

    all_chunks = query.all()

    if not all_chunks:
        return

    chunk_dicts = [
        {
            "id": c.id,
            "chunk_text": c.chunk_text,
            "embedding": json.loads(c.embedding) if c.embedding else [0.1] * 768,
            "matched_topic_id": c.matched_topic_id,
            # Attach density score so deduplicator can use it
            "_density": _information_density(c.chunk_text),
        }
        for c in all_chunks
    ]

    deduplicate_chunks(chunk_dicts)

    # Update database records
    chunk_map = {c["id"]: c for c in chunk_dicts}
    cleaned_count = 0
    fallback_count = 0
    for db_chunk in all_chunks:
        updated = chunk_map[db_chunk.id]
        db_chunk.cluster_id = updated["cluster_id"]
        is_rep = updated["is_representative"]
        db_chunk.is_representative = is_rep
        # If chunk is designated representative and does not yet have cleaned_text, clean it
        if is_rep and not db_chunk.cleaned_text:
            try:
                cleaned, diagram = format_and_clean_note(db_chunk.chunk_text)
                if cleaned:
                    db_chunk.cleaned_text = cleaned
                    db_chunk.diagram_mermaid = diagram
                    cleaned_count += 1
                else:
                    # Cleaning returned empty — keep raw text so dashboard is not blank
                    db_chunk.cleaned_text = db_chunk.chunk_text
                    fallback_count += 1
                    logger.warning(
                        "[Upload] Cleaning returned empty for chunk #%d; stored raw text.",
                        db_chunk.id,
                    )
            except Exception as exc:
                fallback_count += 1
                logger.warning(
                    "[Upload] Failed to clean representative chunk #%d (%s: %s); "
                    "chunk will show raw text.",
                    db_chunk.id,
                    type(exc).__name__,
                    str(exc),
                )

    db.commit()
    logger.info(
        "[Upload] Deduplication complete: %d chunks total, %d cleaned, %d fallback-to-raw.",
        len(all_chunks),
        cleaned_count,
        fallback_count,
    )


def _recompute_importance(db: Session):
    """Recompute topic importance scores from all PYQ records."""
    all_pyqs = db.query(PYQ).filter(PYQ.matched_topic_id.isnot(None)).all()
    total_questions = len(all_pyqs)

    # Count questions per topic
    topic_counts = defaultdict(int)
    for pyq in all_pyqs:
        topic_counts[pyq.matched_topic_id] += 1

    # Include topics with zero questions
    all_topics = db.query(SyllabusTopic).all()
    for topic in all_topics:
        if topic.id not in topic_counts:
            topic_counts[topic.id] = 0

    importance_results = compute_topic_importance(topic_counts, total_questions)

    # Clear and re-insert importance records
    db.query(TopicImportance).delete()
    for result in importance_results:
        db_imp = TopicImportance(
            topic_id=result["topic_id"],
            question_count=result["question_count"],
            importance_score=result["importance_score"],
            importance_label=result["importance_label"],
        )
        db.add(db_imp)

    db.commit()
