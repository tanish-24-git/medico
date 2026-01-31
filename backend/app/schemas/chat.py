"""
Chat Pydantic schemas for API requests and responses.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.chat import MessageRole


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message."""
    content: str = Field(..., min_length=1, max_length=10000)
    role: MessageRole = MessageRole.USER


class ChatMessageResponse(BaseModel):
    """Schema for chat message response."""
    id: int
    session_id: int
    role: MessageRole
    content: str
    created_at: datetime
    token_count: Optional[int] = None
    
    class Config:
        from_attributes = True


class ChatSessionCreate(BaseModel):
    """Schema for creating a chat session."""
    title: Optional[str] = None


class ChatSessionResponse(BaseModel):
    """Schema for chat session response."""
    id: int
    user_id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    
    class Config:
        from_attributes = True


class ChatSessionDetail(ChatSessionResponse):
    """Detailed chat session with messages."""
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Schema for chat request."""
    message: str = Field(..., min_length=1, max_length=10000)
    session_id: Optional[int] = None  # If None, creates new session
    include_reports: bool = True  # Include user's medical reports in context
    stream: bool = True  # Stream response


class ChatStreamResponse(BaseModel):
    """Schema for streaming chat response chunk."""
    content: str
    done: bool = False
    session_id: Optional[int] = None
    message_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Schema for complete chat response (non-streaming)."""
    message: ChatMessageResponse
    session_id: int
