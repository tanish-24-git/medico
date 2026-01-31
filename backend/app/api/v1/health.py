"""
Health check endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Dict, Any

from app.core.dependencies import get_db
from app.db.init_db import check_db_connection
from app.services.groq_service import groq_service
from app.services.pinecone_service import pinecone_service
from loguru import logger


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    version: str = "1.0.0"


class DetailedHealthResponse(BaseModel):
    """Detailed health check response schema."""
    status: str
    version: str
    services: Dict[str, Any]


@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint.
    Returns 200 if service is running.
    """
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """
    Detailed health check including all service dependencies.
    
    Checks:
    - Database connection
    - Groq API connectivity
    - Pinecone connectivity
    """
    services = {}
    overall_status = "healthy"
    
    # Check database
    try:
        db_healthy = await check_db_connection()
        services["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "message": "Connected" if db_healthy else "Connection failed"
        }
        if not db_healthy:
            overall_status = "degraded"
    except Exception as e:
        services["database"] = {
            "status": "unhealthy",
            "message": str(e)
        }
        overall_status = "degraded"
    
    # Check Groq API
    try:
        # Simple test - just check if client is initialized
        groq_healthy = groq_service.client is not None
        services["groq_api"] = {
            "status": "healthy" if groq_healthy else "unhealthy",
            "model": groq_service.model if groq_healthy else None
        }
        if not groq_healthy:
            overall_status = "degraded"
    except Exception as e:
        services["groq_api"] = {
            "status": "unhealthy",
            "message": str(e)
        }
        overall_status = "degraded"
    
    # Check Pinecone
    try:
        pinecone_healthy = pinecone_service.index is not None
        services["pinecone"] = {
            "status": "healthy" if pinecone_healthy else "unhealthy",
            "index": pinecone_service.index_name if pinecone_healthy else None
        }
        if not pinecone_healthy:
            overall_status = "degraded"
    except Exception as e:
        services["pinecone"] = {
            "status": "unhealthy",
            "message": str(e)
        }
        overall_status = "degraded"
    
    return {
        "status": overall_status,
        "version": "1.0.0",
        "services": services
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"ping": "pong"}
