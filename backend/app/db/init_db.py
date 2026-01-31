"""
Database initialization utilities.
"""

from sqlalchemy import text
from loguru import logger

from app.db.base import Base
from app.db.session import engine


async def init_db():
    """
    Initialize database schema.
    Creates all tables if they don't exist.
    """
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


async def check_db_connection():
    """
    Check database connection.
    
    Returns:
        bool: True if connection is successful
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
