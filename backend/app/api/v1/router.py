"""
Main API router aggregating all endpoint modules.
"""

from fastapi import APIRouter

from .health import router as health_router
from .auth import router as auth_router
from .chat import router as chat_router
from .reports import router as reports_router
from .users import router as users_router


# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
