"""
Dependency injection functions for FastAPI.
"""

from typing import AsyncGenerator
from app.db.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    Ensures session is properly closed after request.
    
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
