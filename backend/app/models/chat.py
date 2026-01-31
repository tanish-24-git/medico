"""
Chat session and message models.
"""

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User


class MessageRole(str, enum.Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSession(Base):
    """Chat session model to group related messages."""
    
    __tablename__ = "chat_sessions"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Session metadata
    title: Mapped[str] = mapped_column(String(255), nullable=True)  # Auto-generated from first message
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="chat_sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )
    
    def __repr__(self) -> str:
        return f"<ChatSession(id={self.id}, user_id={self.user_id})>"


class ChatMessage(Base):
    """Individual chat message model."""
    
    __tablename__ = "chat_messages"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign keys
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    
    # Message content
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Metadata
    token_count: Mapped[int] = mapped_column(Integer, nullable=True)  # Track token usage
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")
    
    def __repr__(self) -> str:
        return f"<ChatMessage(id={self.id}, role={self.role}, session_id={self.session_id})>"
