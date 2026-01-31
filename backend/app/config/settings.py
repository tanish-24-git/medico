"""
Application settings and configuration management.
Uses Pydantic Settings for environment variable validation.
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    APP_NAME: str = "MedicoChatbot API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://medico:medico@postgres:5432/medico"
    )
    DB_ECHO: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)
    
    # Firebase Authentication
    FIREBASE_PROJECT_ID: str = Field(...)
    FIREBASE_PRIVATE_KEY: str = Field(...)
    FIREBASE_CLIENT_EMAIL: str = Field(...)
    
    @field_validator("FIREBASE_PRIVATE_KEY")
    @classmethod
    def validate_private_key(cls, v: str) -> str:
        """Replace \\n with actual newlines in private key."""
        return v.replace("\\n", "\n")
    
    # Groq API
    GROQ_API_KEY: str = Field(...)
    GROQ_MODEL: str = Field(default="llama-3.3-70b-versatile")
    GROQ_MAX_TOKENS: int = Field(default=2048)
    GROQ_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)
    
    # Pinecone Vector Database
    PINECONE_API_KEY: str = Field(...)
    PINECONE_ENVIRONMENT: str = Field(default="us-east-1")
    PINECONE_INDEX_NAME: str = Field(default="medico-knowledge")
    PINECONE_DIMENSION: int = Field(default=384)
    
    # File Upload
    UPLOAD_DIR: str = Field(default="./uploads")
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["pdf", "jpg", "jpeg", "png"]
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100)
    RATE_LIMIT_GLOBAL: int = Field(default=1000)
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:3001"]
    
    @field_validator("ALLOWED_ORIGINS", "BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: any) -> List[str]:
        """Convert comma-separated string or list to list of origins."""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://localhost:3001"]
    
    # Monitoring (Optional)
    SENTRY_DSN: Optional[str] = Field(default=None)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL for Alembic."""
        return self.DATABASE_URL.replace("+asyncpg", "")


# Global settings instance
settings = Settings()
