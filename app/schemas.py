"""
Pydantic Schemas for CampusClimb REST API (/api/v1/).

Defines strict request and response contracts for auth, dashboard views,
file uploads, and the bilingual agent endpoint.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field


# --- Auth Schemas ---
class SignUpRequest(BaseModel):
    email: str = Field(..., example="student@campus.edu")
    password: str = Field(..., min_length=6, example="SecurePassword123!")


class LoginRequest(BaseModel):
    email: str = Field(..., example="student@campus.edu")
    password: str = Field(..., example="SecurePassword123!")


class UserResponse(BaseModel):
    id: str
    email: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
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
class AgentQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, example="Explain paging and page table structure")
    subject: str = Field(..., example="Operating Systems")
    language: str = Field("English", example="Hindi")


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
    sources: List[SourceChunkSchema]
