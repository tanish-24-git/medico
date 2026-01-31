"""
Chat endpoints for AI conversations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import json

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSessionResponse,
    ChatSessionDetail,
    ChatMessageResponse
)
from app.services.chat_service import chat_service
from loguru import logger


router = APIRouter()


@router.post("", response_class=StreamingResponse)
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Send chat message and get AI response.
    
    Supports streaming responses for real-time experience.
    """
    try:
        if request.stream:
            # Streaming response
            async def generate():
                async for chunk in chat_service.chat_stream(
                    user=current_user,
                    message=request.message,
                    session_id=request.session_id,
                    include_reports=request.include_reports,
                    db=db
                ):
                    yield f"data: {json.dumps(chunk)}\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            # Non-streaming response (for compatibility)
            full_response = ""
            session_id = None
            message_id = None
            
            async for chunk in chat_service.chat_stream(
                user=current_user,
                message=request.message,
                session_id=request.session_id,
                include_reports=request.include_reports,
                db=db
            ):
                if chunk.get("content"):
                    full_response += chunk["content"]
                if chunk.get("session_id"):
                    session_id = chunk["session_id"]
                if chunk.get("message_id"):
                    message_id = chunk["message_id"]
            
            # Get the saved message
            if message_id:
                result = await db.execute(
                    select(ChatMessage).where(ChatMessage.id == message_id)
                )
                message = result.scalar_one()
                
                return ChatResponse(
                    message=ChatMessageResponse.from_orm(message),
                    session_id=session_id
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to save message"
                )
            
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """
    List user's chat sessions.
    """
    try:
        # Get sessions with message count
        result = await db.execute(
            select(
                ChatSession,
                func.count(ChatMessage.id).label("message_count")
            )
            .outerjoin(ChatMessage, ChatSession.id == ChatMessage.session_id)
            .where(ChatSession.user_id == current_user.id)
            .group_by(ChatSession.id)
            .order_by(ChatSession.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        sessions = []
        for session, msg_count in result:
            session_dict = ChatSessionResponse.from_orm(session).model_dump()
            session_dict["message_count"] = msg_count
            sessions.append(ChatSessionResponse(**session_dict))
        
        return sessions
        
    except Exception as e:
        logger.error(f"Session list error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


@router.get("/sessions/{session_id}", response_model=ChatSessionDetail)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get chat session with all messages.
    """
    try:
        # Get session
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.id == session_id)
            .where(ChatSession.user_id == current_user.id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get messages
        messages_result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
        )
        messages = messages_result.scalars().all()
        
        # Build response
        session_dict = ChatSessionResponse.from_orm(session).model_dump()
        session_dict["messages"] = [
            ChatMessageResponse.from_orm(msg) for msg in messages
        ]
        session_dict["message_count"] = len(messages)
        
        return ChatSessionDetail(**session_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session get error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session: {str(e)}"
        )


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete chat session and all its messages.
    """
    try:
        # Get session
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.id == session_id)
            .where(ChatSession.user_id == current_user.id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Delete session (cascades to messages)
        await db.delete(session)
        await db.commit()
        
        logger.info(f"Deleted session {session_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session delete error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 50
):
    """
    Get chat history for a session.
    """
    try:
        # Verify session belongs to user
        session_result = await db.execute(
            select(ChatSession)
            .where(ChatSession.id == session_id)
            .where(ChatSession.user_id == current_user.id)
        )
        session = session_result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get messages
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
        )
        messages = result.scalars().all()
        
        return [ChatMessageResponse.from_orm(msg) for msg in messages]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"History get error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}"
        )
