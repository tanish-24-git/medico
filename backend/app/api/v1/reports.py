"""
Medical report upload and analysis endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.report import MedicalReport
from app.schemas.report import (
    ReportUploadResponse,
    ReportResponse,
    ReportAnalysis,
    ReportListResponse
)
from app.services.report_processor import report_processor
from app.services.pinecone_service import pinecone_service
from loguru import logger


router = APIRouter()


@router.post("/upload", response_model=ReportUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_report(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload medical report (PDF or image).
    
    Accepts: PDF, JPG, JPEG, PNG
    """
    try:
        # Read file
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file
        is_valid, error = report_processor.validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error
            )
        
        # Save file
        file_path = await report_processor.save_file(
            file_content,
            file.filename,
            current_user.id
        )
        
        # Get file type
        file_type = file.filename.rsplit('.', 1)[-1].lower()
        
        # Create database record
        report = MedicalReport(
            user_id=current_user.id,
            filename=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            processing_status="pending"
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        
        # Process asynchronously (in background)
        # For now, process immediately
        try:
            # Extract text
            extracted_text = await report_processor.extract_text(file_path, file_type)
            report.extracted_text = extracted_text
            
            # Parse metrics
            parsed_metrics = await report_processor.parse_medical_metrics(extracted_text)
            report.parsed_metrics = parsed_metrics
            
            # AI analysis
            if extracted_text:
                analysis = await report_processor.analyze_report(extracted_text)
                report.ai_summary = analysis.get("summary", "")
                report.ai_insights = analysis
            
            report.processing_status = "completed"
            
            # Index in Pinecone for RAG
            if report.ai_summary:
                await pinecone_service.upsert_user_report(
                    report_id=report.id,
                    user_id=current_user.id,
                    report_text=extracted_text,
                    report_summary=report.ai_summary
                )
            
        except Exception as e:
            logger.error(f"Report processing error: {str(e)}")
            report.processing_status = "failed"
        
        await db.commit()
        await db.refresh(report)
        
        logger.info(f"Uploaded report {report.id} for user {current_user.email}")
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("", response_model=ReportListResponse)
async def list_reports(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    page_size: int = 10
):
    """
    List user's medical reports.
    """
    try:
        # Get total count
        count_result = await db.execute(
            select(MedicalReport)
            .where(MedicalReport.user_id == current_user.id)
        )
        total = len(count_result.scalars().all())
        
        # Get paginated reports
        offset = (page - 1) * page_size
        result = await db.execute(
            select(MedicalReport)
            .where(MedicalReport.user_id == current_user.id)
            .order_by(MedicalReport.created_at.desc())
            .limit(page_size)
            .offset(offset)
        )
        reports = result.scalars().all()
        
        return ReportListResponse(
            reports=[ReportResponse.from_orm(r) for r in reports],
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Report list error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list reports: {str(e)}"
        )


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific medical report details.
    """
    try:
        result = await db.execute(
            select(MedicalReport)
            .where(MedicalReport.id == report_id)
            .where(MedicalReport.user_id == current_user.id)
        )
        report = result.scalar_one_or_none()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report get error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get report: {str(e)}"
        )


@router.get("/{report_id}/analysis", response_model=ReportAnalysis)
async def get_report_analysis(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI analysis of medical report.
    """
    try:
        result = await db.execute(
            select(MedicalReport)
            .where(MedicalReport.id == report_id)
            .where(MedicalReport.user_id == current_user.id)
        )
        report = result.scalar_one_or_none()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        if not report.ai_insights:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not available for this report"
            )
        
        # Convert ai_insights to ReportAnalysis schema
        return ReportAnalysis(
            summary=report.ai_insights.get("summary", ""),
            key_findings=report.ai_insights.get("key_findings", []),
            abnormal_values=report.ai_insights.get("abnormal_values", []),
            recommendations=report.ai_insights.get("recommendations", []),
            risk_assessment=report.ai_insights.get("risk_assessment")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis get error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis: {str(e)}"
        )


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete medical report and associated file.
    """
    try:
        result = await db.execute(
            select(MedicalReport)
            .where(MedicalReport.id == report_id)
            .where(MedicalReport.user_id == current_user.id)
        )
        report = result.scalar_one_or_none()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        # Delete file from disk
        await report_processor.delete_file(report.file_path)
        
        # Delete from database
        await db.delete(report)
        await db.commit()
        
        logger.info(f"Deleted report {report_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report delete error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )
