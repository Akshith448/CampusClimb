"""
Authentication Router — Managed Supabase Auth REST Endpoints (/api/v1/auth/).

Provides signup, login, and current user profile endpoints using Supabase Auth.
"""

from typing import Dict, Any

from fastapi import APIRouter, Depends, status

from app.auth import get_current_user, supabase_login, supabase_signup
from app.schemas import AuthTokenResponse, LoginRequest, SignUpRequest, UserResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: SignUpRequest):
    """Register a new user account via Supabase Auth."""
    result = supabase_signup(body.email, body.password)
    return AuthTokenResponse(
        access_token=result["access_token"],
        token_type="bearer",
        user=UserResponse(**result["user"]),
    )


@router.post("/login", response_model=AuthTokenResponse)
async def login(body: LoginRequest):
    """Authenticate an existing user account via Supabase Auth."""
    result = supabase_login(body.email, body.password)
    return AuthTokenResponse(
        access_token=result["access_token"],
        token_type="bearer",
        user=UserResponse(**result["user"]),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve details for the currently authenticated JWT user."""
    return UserResponse(
        id=current_user.get("id", ""),
        email=current_user.get("email", ""),
    )
