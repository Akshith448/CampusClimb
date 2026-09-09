"""
Authentication & JWT Middleware — Managed Supabase Auth Integration.

Provides authentication helper functions that route signup and login directly through
Supabase's Auth REST API, and a FastAPI dependency (`get_current_user`) for validating
Bearer JWT tokens against SUPABASE_JWT_SECRET.
"""

import os
from typing import Dict, Any

import jwt
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "").strip()
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "").strip()

security = HTTPBearer(auto_error=False)


def _mask(val: str) -> str:
    """Return masked string preview for logging (first 4 chars + ****)."""
    return f"{val[:4]}****" if val and len(val) >= 4 else "(not set)"


def print_env_auth_status():
    """Print masked environment configuration status."""
    print(f"   [AUTH CFG] SUPABASE_URL: {_mask(SUPABASE_URL)}")
    print(f"   [AUTH CFG] SUPABASE_ANON_KEY: {_mask(SUPABASE_ANON_KEY)}")
    print(f"   [AUTH CFG] SUPABASE_JWT_SECRET: {_mask(SUPABASE_JWT_SECRET)}")


def supabase_signup(email: str, password: str) -> Dict[str, Any]:
    """Register a new user via real Supabase Auth REST API."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase credentials (SUPABASE_URL, SUPABASE_ANON_KEY) are not configured in .env",
        )

    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/signup"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload = {"email": email, "password": password}

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        data = res.json()
        if res.status_code >= 400:
            msg = data.get("msg") or data.get("error_description") or data.get("message") or "Signup failed"
            raise HTTPException(status_code=res.status_code, detail=msg)

        user_data = data.get("user") or {}
        session = data.get("session") or {}
        access_token = data.get("access_token") or session.get("access_token") or ""

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_data.get("id", ""),
                "email": user_data.get("email", email),
            },
        }
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to communicate with Supabase Auth service: {str(e)}",
        )


def supabase_login(email: str, password: str) -> Dict[str, Any]:
    """Authenticate an existing user via real Supabase Auth REST API."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase credentials (SUPABASE_URL, SUPABASE_ANON_KEY) are not configured in .env",
        )

    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload = {"email": email, "password": password}

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        data = res.json()
        if res.status_code >= 400:
            msg = data.get("error_description") or data.get("msg") or data.get("message") or "Invalid login credentials"
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

        user_data = data.get("user") or {}
        access_token = data.get("access_token") or ""

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_data.get("id", ""),
                "email": user_data.get("email", email),
            },
        }
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to communicate with Supabase Auth service: {str(e)}",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """FastAPI dependency that extracts and validates the Bearer JWT token against SUPABASE_JWT_SECRET."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization Header Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not SUPABASE_JWT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SUPABASE_JWT_SECRET is not configured in .env",
        )

    # Validate JWT signature against SUPABASE_JWT_SECRET
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        return {
            "id": payload.get("sub", ""),
            "email": payload.get("email", ""),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
