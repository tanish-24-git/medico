"""
User database model.
"""

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    """User model for authenticated users."""
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Firebase authentication
    firebase_uid: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    
    # User information
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=True)
    photo_url: Mapped[str] = mapped_column(String(512), nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        "ChatSession", back_populates="user", cascade="all, delete-orphan"
    )
    medical_reports: Mapped[list["MedicalReport"]] = relationship(
        "MedicalReport", back_populates="user", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
