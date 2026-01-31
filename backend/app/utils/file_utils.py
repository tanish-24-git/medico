"""
File utility functions.
"""

from pathlib import Path
from loguru import logger


def ensure_directory_exists(directory: str) -> Path:
    """
    Ensure directory exists, create if not.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {path}")
    return path


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        Size in MB
    """
    size_bytes = Path(file_path).stat().st_size
    return size_bytes / (1024 * 1024)


def delete_file_if_exists(file_path: str) -> bool:
    """
    Delete file if it exists.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if deleted, False if didn't exist
    """
    path = Path(file_path)
    if path.exists():
        path.unlink()
        logger.info(f"Deleted file: {file_path}")
        return True
    return False
