# Scripts for common development tasks

## Start Development Environment
**Windows:**
```powershell
# Copy environment file
Copy-Item .env.example .env

# Edit .env with your API keys

# Start all services
docker-compose up --build
```

**Linux/Mac:**
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API keys

# Start all services
docker-compose up --build
```

## Stop Services
```bash
docker-compose down
```

## View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## Reset Database
```bash
docker-compose down -v
docker-compose up --build
```

## Access Services
- Frontend: http://localhost
- Backend API: http://localhost/api/v1
- API Documentation: http://localhost/docs
- Database: localhost:5432

## Production Deployment

1. Set all environment variables in `.env`
2. Ensure `ENVIRONMENT=production`
3. Run: `docker-compose up -d --build`
4. Monitor: `docker-compose logs -f`

## Troubleshooting

### Port conflicts
```bash
docker-compose down
# Check which process is using the port
# Windows: netstat -ano | findstr "PORT"
# Linux/Mac: lsof -i :PORT
```

### Container not starting
```bash
docker-compose down
docker-compose up --build
docker-compose logs SERVICE_NAME
```

### Database issues
```bash
docker-compose down -v  # WARNING: Deletes all data
docker-compose up --build
```
