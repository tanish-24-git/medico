"""
User profile endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.chat import ChatSession
from app.models.report import MedicalReport
from app.schemas.user import UserResponse, UserUpdate, UserProfile
from app.services.auth_service import auth_service
from loguru import logger


router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's profile with statistics.
    """
    try:
        # Get total reports
        reports_result = await db.execute(
            select(func.count(MedicalReport.id))
            .where(MedicalReport.user_id == current_user.id)
        )
        total_reports = reports_result.scalar()
        
        # Get total chat sessions
        sessions_result = await db.execute(
            select(func.count(ChatSession.id))
            .where(ChatSession.user_id == current_user.id)
        )
        total_sessions = sessions_result.scalar()
        
        # Build profile response
        profile_dict = UserResponse.from_orm(current_user).model_dump()
        profile_dict["total_reports"] = total_reports or 0
        profile_dict["total_chat_sessions"] = total_sessions or 0
        
        return UserProfile(**profile_dict)
        
    except Exception as e:
        logger.error(f"Profile get error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile.
    """
    try:
        user = await auth_service.update_user_profile(
            user=current_user,
            display_name=update_data.display_name,
            db=db
        )
        
        return user
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete current user's account and all associated data.
    
    Warning: This action is irreversible.
    """
    try:
        # Delete user reports from vector database
        await pinecone_service.delete_user_reports(current_user.id)
        
        # Delete user account (cascades to sessions, messages, reports)
        success = await auth_service.delete_user(current_user, db)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete account"
            )
        
        logger.info(f"Account deleted: {current_user.email}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Account deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete account: {str(e)}"
        )


# Import at the end to avoid circular dependency
from app.services.pinecone_service import pinecone_service
