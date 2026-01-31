"""
Medical report model.
"""

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .user import User


class MedicalReport(Base):
    """Medical report model for uploaded health documents."""
    
    __tablename__ = "medical_reports"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # File information
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pdf, jpg, png
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)  # in bytes
    
    # Extracted content
    extracted_text: Mapped[str] = mapped_column(Text, nullable=True)  # OCR/PDF text
    
    # Parsed medical data (JSON)
    parsed_metrics: Mapped[dict] = mapped_column(JSON, nullable=True)  # Blood pressure, sugar, etc.
    
    # AI Analysis
    ai_summary: Mapped[str] = mapped_column(Text, nullable=True)
    ai_insights: Mapped[dict] = mapped_column(JSON, nullable=True)  # AI-generated insights
    
    # Processing status
    processing_status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, processing, completed, failed
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="medical_reports")
    
    def __repr__(self) -> str:
        return f"<MedicalReport(id={self.id}, filename={self.filename}, user_id={self.user_id})>"
