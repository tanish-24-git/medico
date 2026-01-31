"""
Database session management with SQLAlchemy async support.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config.settings import settings
from loguru import logger


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    future=True,
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    """
    Dependency to get database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()
