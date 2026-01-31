"""
Medical Report Pydantic schemas for API requests and responses.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ReportUploadResponse(BaseModel):
    """Schema for report upload response."""
    id: int
    filename: str
    file_size: int
    file_type: str
    processing_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    """Schema for medical report response."""
    id: int
    user_id: int
    filename: str
    file_type: str
    file_size: int
    extracted_text: Optional[str] = None
    parsed_metrics: Optional[Dict[str, Any]] = None
    ai_summary: Optional[str] = None
    ai_insights: Optional[Dict[str, Any]] = None
    processing_status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReportAnalysis(BaseModel):
    """Schema for AI analysis of medical report."""
    summary: str
    key_findings: List[str]
    abnormal_values: List[Dict[str, Any]]
    recommendations: List[str]
    risk_assessment: Optional[str] = None


class ReportMetric(BaseModel):
    """Schema for a single medical metric."""
    name: str
    value: str
    unit: Optional[str] = None
    status: str  # normal, warning, alert
    reference_range: Optional[str] = None
    interpretation: Optional[str] = None


class ReportListResponse(BaseModel):
    """Schema for listing reports."""
    reports: List[ReportResponse]
    total: int
    page: int = 1
    page_size: int = 10
