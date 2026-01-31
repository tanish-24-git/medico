"""
Security utilities for authentication and authorization.
Implements Firebase token verification and user dependency injection.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.firebase import firebase_config
from app.core.dependencies import get_db
from app.models.user import User
from app.db.session import async_session
from loguru import logger


# Security scheme
security = HTTPBearer()


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify Firebase ID token from Authorization header.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        decoded_token = firebase_config.verify_token(token)
        return decoded_token
    except ValueError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token_data: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from database.
    Creates user if doesn't exist (first-time login).
    
    Args:
        token_data: Decoded Firebase token
        db: Database session
        
    Returns:
        User object from database
        
    Raises:
        HTTPException: If user cannot be retrieved or created
    """
    from sqlalchemy import select
    
    try:
        firebase_uid = token_data.get("uid")
        email = token_data.get("email")
        
        if not firebase_uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Try to get existing user
        result = await db.execute(
            select(User).where(User.firebase_uid == firebase_uid)
        )
        user = result.scalar_one_or_none()
        
        # Create user if doesn't exist (first-time login)
        if not user:
            user = User(
                firebase_uid=firebase_uid,
                email=email,
                display_name=token_data.get("name"),
                photo_url=token_data.get("picture"),
                email_verified=token_data.get("email_verified", False)
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"Created new user: {email}")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve user information"
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Useful for endpoints that work with or without authentication.
    
    Args:
        credentials: Optional HTTP Bearer credentials
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        token_data = firebase_config.verify_token(credentials.credentials)
        firebase_uid = token_data.get("uid")
        
        result = await db.execute(
            select(User).where(User.firebase_uid == firebase_uid)
        )
        return result.scalar_one_or_none()
    except Exception:
        return None


def check_user_permissions(user: User, required_role: str = "user") -> bool:
    """
    Check if user has required permissions.
    Can be extended for role-based access control.
    
    Args:
        user: User object
        required_role: Required role (currently unused, for future RBAC)
        
    Returns:
        True if user has permissions
    """
    # Future: Implement RBAC here
    # For now, all authenticated users have access
    return user is not None
