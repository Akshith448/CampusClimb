"""
Pydantic Schemas for CampusClimb REST API (/api/v1/).

Defines strict request and response contracts for auth, dashboard views,
file uploads, and the bilingual agent endpoint.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# Standard regex for email validation without third-party email_validator package
EMAIL_REGEX = r"^[\w\.\+\-]+@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+$"


# --- Auth Schemas ---
class SignUpRequest(BaseModel):
    email: str = Field(
        ...,
        pattern=EMAIL_REGEX,
        description="User email address",
        json_schema_extra={"example": "student@campus.edu"},
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (minimum 8 characters)",
        json_schema_extra={"example": "SecurePassword123!"},
    )


class LoginRequest(BaseModel):
    email: str = Field(
        ...,
        pattern=EMAIL_REGEX,
        description="User email address",
        json_schema_extra={"example": "student@campus.edu"},
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="User password",
        json_schema_extra={"example": "SecurePassword123!"},
    )


class UserResponse(BaseModel):
    id: str
    email: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    user: UserResponse


# --- System Stats & Dashboard Schemas ---
class StatsResponse(BaseModel):
    syllabus_count: int
    notes_count: int
    pyq_count: int
    supported_subjects: List[str]


class TopicSummary(BaseModel):
    id: int
    subject: str
    unit_number: int
    unit_name: str
    topic_name: str
    importance_score: float
    importance_label: str
    question_count: int
    chunk_count: int
    notes: List[str]


class DashboardStats(BaseModel):
    total_chunks: int
    useful_chunks: int
    filtered_chunks: int
    dedup_reduction: float
    avg_confidence: float


class DashboardResponse(BaseModel):
    topics: List[TopicSummary]
    supported_subjects: List[str]
    selected_subject: Optional[str] = None
    stats: DashboardStats


# --- Topic Detail Schemas ---
class ChunkDetail(BaseModel):
    id: int
    chunk_text: str
    student_name: str
    similarity_score: Optional[float] = None
    cluster_id: Optional[int] = None
    is_representative: bool
    confidence: Optional[str] = None
    margin: Optional[float] = None
    chunk_type: Optional[str] = None


class PYQDetail(BaseModel):
    id: int
    question_text: str
    year: int
    confidence: Optional[str] = None


class TopicDetail(BaseModel):
    id: int
    subject: str
    unit_number: int
    unit_name: str
    topic_name: str
    representative_notes: str


class TopicImportanceDetail(BaseModel):
    score: float
    label: str
    question_count: int


class TopicDetailResponse(BaseModel):
    topic: Optional[TopicDetail] = None
    importance: Optional[TopicImportanceDetail] = None
    high_med_chunks: List[ChunkDetail]
    mixed_chunks: List[ChunkDetail]
    low_chunks: List[ChunkDetail]
    clusters: Dict[str, List[ChunkDetail]]
    key_concepts: List[str]
    pyqs: List[PYQDetail]
    total_chunks: int


# --- Upload Schemas ---
class UploadResponse(BaseModel):
    status: str = "success"
    message: str
    details: Optional[Dict[str, Any]] = None


# --- Bilingual Agent Schemas ---
class CitationItem(BaseModel):
    citation_id: int
    source_id: int
    source_name: str
    chunk_id: int
    page_number: Optional[int] = None
    snippet: str
    similarity_score: Optional[float] = None


class SourceItemSchema(BaseModel):
    id: int
    filename: str
    student_name: Optional[str] = None
    upload_date: Optional[str] = None
    chunk_count: int = 0


class SourceListResponse(BaseModel):
    subject: str
    sources: List[SourceItemSchema]


class AgentQueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Query or question from the student",
        json_schema_extra={"example": "Explain paging and page table structure"},
    )
    subject: str = Field(
        "Operating Systems",
        min_length=1,
        max_length=100,
        description="Subject name",
        json_schema_extra={"example": "Operating Systems"},
    )
    language: Optional[str] = Field(
        "auto",
        max_length=50,
        description="Target response language",
        json_schema_extra={"example": "auto"},
    )
    selected_source_ids: Optional[List[int]] = Field(
        None,
        description="Specific source Note IDs to restrict retrieval to. If omitted, all user sources for the subject are used.",
    )
    chat_history: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Optional recent conversation turns for context continuity.",
    )


class SourceChunkSchema(BaseModel):
    id: int
    text: str
    similarity_score: Optional[float] = None


class AgentQueryResponse(BaseModel):
    query: str
    subject: str
    language: str
    matched_topic: str
    confidence_score: float
    confidence_label: str
    answer: str
    explanation: str
    sources: List[SourceChunkSchema] = Field(default_factory=list)
    selected_source_ids: Optional[List[int]] = None
    source_type: str = "notes"  # "notes" | "general_knowledge"
    notes_match: bool = True
    fallback_used: bool = False
    notice: Optional[str] = None
    citations: List[CitationItem] = Field(default_factory=list)
    diagram_mermaid: Optional[str] = None
    related_questions: List[str] = Field(default_factory=list)

