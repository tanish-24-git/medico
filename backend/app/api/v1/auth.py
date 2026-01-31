"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.dependencies import get_db
from app.core.security import get_current_user, verify_firebase_token
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.auth_service import auth_service


router = APIRouter()


class GoogleAuthRequest(BaseModel):
    """Google sign-in request schema."""
    id_token: str


@router.post("/google", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def google_sign_in(
    request: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate with Google sign-in.
    
    Verifies Firebase ID token and creates/updates user in database.
    """
    from loguru import logger
    logger.info("Google sign-in request received")

    try:
        # Import here to avoid circular dependency
        from app.config.firebase import firebase_config
        
        # Verify token
        token_data = firebase_config.verify_token(request.id_token)
        
        # Get or create user
        user = await auth_service.get_or_create_user(
            firebase_uid=token_data.get("uid"),
            email=token_data.get("email"),
            display_name=token_data.get("name"),
            photo_url=token_data.get("picture"),
            email_verified=token_data.get("email_verified", False),
            db=db
        )
        
        return user
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    """
    return current_user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout endpoint.
    
    Note: Firebase handles token invalidation on client side.
    This endpoint is mainly for logging purposes.
    """
    from loguru import logger
    logger.info(f"User logged out: {current_user.email}")
    
    return {"message": "Logged out successfully"}


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    token_data: dict = Depends(verify_firebase_token)
):
    """
    Refresh authentication token.
    
    Note: Firebase handles token refresh on client side.
    This endpoint verifies the new token is valid.
    """
    return {
        "message": "Token is valid",
        "uid": token_data.get("uid")
    }
