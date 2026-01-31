"""
Authentication service for user management.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.models.user import User
from app.config.firebase import firebase_config


class AuthService:
    """Service for authentication and user management."""
    
    async def get_or_create_user(
        self,
        firebase_uid: str,
        email: str,
        display_name: Optional[str],
        photo_url: Optional[str],
        email_verified: bool,
        db: AsyncSession
    ) -> User:
        """
        Get existing user or create new one.
        
        Args:
            firebase_uid: Firebase user ID
            email: User email
            display_name: User display name
            photo_url: User photo URL
            email_verified: Email verification status
            db: Database session
            
        Returns:
            User object
        """
        try:
            # Try to get existing user
            result = await db.execute(
                select(User).where(User.firebase_uid == firebase_uid)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # Update last login
                from datetime import datetime
                user.last_login = datetime.utcnow()
                
                # Update user info if changed
                if user.display_name != display_name:
                    user.display_name = display_name
                if user.photo_url != photo_url:
                    user.photo_url = photo_url
                if user.email_verified != email_verified:
                    user.email_verified = email_verified
                
                await db.commit()
                await db.refresh(user)
                
                logger.info(f"User logged in: {email}")
            else:
                # Create new user
                user = User(
                    firebase_uid=firebase_uid,
                    email=email,
                    display_name=display_name,
                    photo_url=photo_url,
                    email_verified=email_verified
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
                
                logger.info(f"New user created: {email}")
            
            return user
            
        except Exception as e:
            logger.error(f"User creation/retrieval error: {str(e)}")
            raise
    
    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> Optional[User]:
        """
        Get user by database ID.
        
        Args:
            user_id: User database ID
            db: Database session
            
        Returns:
            User object or None
        """
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"User retrieval error: {str(e)}")
            return None
    
    async def update_user_profile(
        self,
        user: User,
        display_name: Optional[str],
        db: AsyncSession
    ) -> User:
        """
        Update user profile.
        
        Args:
            user: User object
            display_name: New display name
            db: Database session
            
        Returns:
            Updated user object
        """
        try:
            if display_name is not None:
                user.display_name = display_name
            
            from datetime import datetime
            user.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"User profile updated: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            raise
    
    async def delete_user(self, user: User, db: AsyncSession) -> bool:
        """
        Delete user and all associated data.
        
        Args:
            user: User object
            db: Database session
            
        Returns:
            Success status
        """
        try:
            # Delete from database (cascades to sessions, messages, reports)
            await db.delete(user)
            await db.commit()
            
            logger.info(f"User deleted: {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"User deletion error: {str(e)}")
            await db.rollback()
            return False


# Global instance
auth_service = AuthService()
