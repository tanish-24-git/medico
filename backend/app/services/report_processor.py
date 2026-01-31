"""
Medical report processing service.
Handles PDF/image upload, OCR, text extraction, and AI analysis.
"""

import os
import re
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import pypdf
from PIL import Image
import pytesseract
from loguru import logger

from app.config.settings import settings
from app.services.groq_service import groq_service


class ReportProcessor:
    """Service for processing medical reports."""
    
    def __init__(self):
        """Initialize report processor."""
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    def validate_file(self, filename: str, file_size: int) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file.
        
        Args:
            filename: Name of the file
            file_size: Size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file extension
        extension = filename.rsplit('.', 1)[-1].lower()
        if extension not in self.allowed_extensions:
            return False, f"File type not allowed. Allowed: {', '.join(self.allowed_extensions)}"
        
        # Check file size
        if file_size > settings.MAX_UPLOAD_SIZE:
            max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb}MB"
        
        return True, None
    
    async def save_file(self, file_content: bytes, filename: str, user_id: int) -> str:
        """
        Save uploaded file to disk.
        
        Args:
            file_content: File bytes
            filename: Original filename
            user_id: User ID for organization
            
        Returns:
            Saved file path
        """
        try:
            # Create user directory
            user_dir = self.upload_dir / str(user_id)
            user_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate safe filename
            safe_filename = self._sanitize_filename(filename)
            
            # Add timestamp to avoid conflicts
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = safe_filename.rsplit('.', 1)
            unique_filename = f"{name}_{timestamp}.{ext}"
            
            file_path = user_dir / unique_filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            logger.info(f"Saved file: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"File save error: {str(e)}")
            raise
    
    def _sanitize_filename(self, filename: str) -> str:
        """Remove potentially dangerous characters from filename."""
        # Keep only alphanumeric, dash, underscore, and dot
        filename = re.sub(r'[^\w\s.-]', '', filename)
        return filename.strip()
    
    async def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text.strip()
            
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise
    
    async def extract_text_from_image(self, file_path: str) -> str:
        """
        Extract text from image using OCR (Tesseract).
        
        Args:
            file_path: Path to image file
            
        Returns:
            Extracted text
        """
        try:
            # Open image
            image = Image.open(file_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            logger.info(f"Extracted {len(text)} characters from image via OCR")
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR extraction error: {str(e)}")
            # Return empty if OCR fails (tesseract might not be installed)
            logger.warning("OCR failed - Tesseract might not be installed")
            return ""
    
    async def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from file based on type.
        
        Args:
            file_path: Path to file
            file_type: File extension
            
        Returns:
            Extracted text
        """
        try:
            if file_type == 'pdf':
                return await self.extract_text_from_pdf(file_path)
            elif file_type in ['jpg', 'jpeg', 'png']:
                return await self.extract_text_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Text extraction error: {str(e)}")
            raise
    
    async def parse_medical_metrics(self, text: str) -> Dict[str, Any]:
        """
        Parse medical metrics from report text.
        
        Args:
            text: Extracted report text
            
        Returns:
            Dictionary of parsed metrics
        """
        metrics = {}
        
        # Common patterns for medical values
        patterns = {
            'blood_pressure': r'(?:BP|Blood Pressure)[:\s]+(\d{2,3})/(\d{2,3})',
            'pulse': r'(?:Pulse|Heart Rate|HR)[:\s]+(\d{2,3})',
            'glucose': r'(?:Glucose|Blood Sugar|BS)[:\s]+(\d{2,3})',
            'cholesterol': r'(?:Cholesterol|Chol)[:\s]+(\d{2,3})',
            'hemoglobin': r'(?:Hemoglobin|Hb|HGB)[:\s]+(\d+\.?\d*)',
        }
        
        for metric_name, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if metric_name == 'blood_pressure':
                    metrics[metric_name] = f"{match.group(1)}/{match.group(2)}"
                else:
                    metrics[metric_name] = match.group(1)
        
        logger.info(f"Parsed {len(metrics)} medical metrics")
        return metrics
    
    async def analyze_report(
        self,
        extracted_text: str,
        user_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze medical report using AI.
        
        Args:
            extracted_text: Text extracted from report
            user_context: Optional user medical context
            
        Returns:
            AI analysis results
        """
        try:
            logger.info(f"Starting AI analysis for report with {len(extracted_text)} chars")
            # Use Groq service for analysis
            analysis = await groq_service.analyze_medical_report(
                extracted_text,
                user_context
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Report analysis error: {str(e)}")
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from disk.
        
        Args:
            file_path: Path to file
            
        Returns:
            Success status
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"File deletion error: {str(e)}")
            return False


# Global instance
report_processor = ReportProcessor()
