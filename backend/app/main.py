"""
MedicoChatbot FastAPI Application
Main entry point for the backend API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.config.settings import settings
from app.config.firebase import firebase_config
from app.core.middleware import (
    RequestLoggingMiddleware,
    limiter,
    rate_limit_exceeded_handler
)
from app.api.v1.router import api_router
from app.db.init_db import init_db
from app.utils.logger import setup_logger
from app.utils.file_utils import ensure_directory_exists
from loguru import logger


# Setup logging
setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting MedicoChatbot API...")
    
    try:
        # Initialize Firebase
        firebase_config.initialize()
        logger.info("✓ Firebase initialized")
        
        # Initialize database
        await init_db()
        logger.info("✓ Database initialized")
        
        # Ensure upload directory exists
        ensure_directory_exists(settings.UPLOAD_DIR)
        logger.info(f"✓ Upload directory ready: {settings.UPLOAD_DIR}")
        
        logger.info(f"🚀 MedicoChatbot API started successfully on {settings.ENVIRONMENT} mode")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down MedicoChatbot API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Industry-grade backend for MedicoChatbot - AI-powered medical report analysis and chat assistant",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add rate limiter state
app.state.limiter = limiter

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"]
)

# Add custom middleware
app.add_middleware(RequestLoggingMiddleware)


# Exception handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors."""
    return await rate_limit_exceeded_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # Don't expose internal errors in production
    if settings.ENVIRONMENT == "production":
        detail = "An internal error occurred"
    else:
        detail = str(exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": detail
        }
    )


# Include API router
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else "disabled",
    }


# Health check (simple, no prefix)
@app.get("/health", tags=["health"])
async def health():
    """Quick health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
