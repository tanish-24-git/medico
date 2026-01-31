# Backend API

FastAPI backend for MedicoChatbot with enterprise-grade architecture.

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Project Structure

```
app/
├── api/v1/          # API endpoints
├── core/            # Core functionality (security, middleware)
├── models/          # Database models
├── schemas/         # Pydantic schemas
├── services/        # Business logic
├── db/              # Database configuration
├── config/          # Settings
└── utils/           # Utilities
```

## Environment Variables

See `../.env.example` for required environment variables.
