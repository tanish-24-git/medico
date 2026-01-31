"""
Input validation utilities.
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input by removing potentially harmful characters.
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Strip whitespace
    text = text.strip()
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_filename(filename: str) -> bool:
    """
    Validate filename for security.
    
    Args:
        filename: Filename to validate
        
    Returns:
        True if safe, False otherwise
    """
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    # Check for valid characters
    pattern = r'^[\w\s.-]+$'
    return bool(re.match(pattern, filename))
