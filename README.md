# 🏥 MedicoChatbot - AI Medical Assistant

An industry-grade, full-stack application for analyzing medical reports and providing AI-powered health insights in simple language.

## 🌟 Features

### Backend (FastAPI)
- **🔐 Firebase Authentication** - Secure Google sign-in
- **💬 AI Chat** - Streaming responses powered by Groq LLM (Llama 3.3 70B)
- **📄 Report Analysis** - PDF/Image OCR with AI-powered medical insights
- **🔍 RAG System** - Pinecone vector database for contextual medical knowledge
- **🗄️ PostgreSQL Database** - Async SQLAlchemy ORM
- **🛡️ Enterprise Security** - Rate limiting, CORS, input validation, security headers
- **📊 Monitoring** - Health checks, structured logging, error tracking

### Frontend (Next.js)
- **⚡ Modern UI** - Built with Next.js 16, React 19, and TailwindCSS 4
- **🎨 Beautiful Components** - shadcn/ui with Radix primitives
- **📱 Responsive Design** - Mobile-first approach
- **🌓 Dark Mode** - Theme switching support

## 🏗️ Architecture

```
medico/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # REST API endpoints
│   │   ├── core/           # Security, middleware, dependencies
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── db/             # Database configuration
│   │   ├── config/         # Settings & Firebase
│   │   └── utils/          # Utilities
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Next.js frontend
│   ├── app/                # Next.js 16 app directory
│   ├── components/         # React components
│   ├── Dockerfile
│   └── package.json
├── nginx/                   # Nginx reverse proxy
│   └── nginx.conf
├── docker-compose.yml
└── .env.example

```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- API Keys:
  - [Groq API Key](https://console.groq.com)
  - [Pinecone API Key](https://www.pinecone.io)
  - [Firebase Project](https://console.firebase.google.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd medico
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and fill in your API keys:
   - `GROQ_API_KEY` - Get from Groq Console
   - `PINECONE_API_KEY` - Get from Pinecone Dashboard
   - `FIREBASE_*` - Get from Firebase Project Settings > Service Accounts
   - `SECRET_KEY` - Generate a secure random string (32+ characters)

3. **Configure Firebase**
   - Go to [Firebase Console](https://console.firebase.google.com)
   - Create a new project or use existing
   - Enable Authentication > Google sign-in
   - Go to Project Settings > Service Accounts
   - Generate new private key (JSON)
   - Copy credentials to `.env`:
     ```env
     FIREBASE_PROJECT_ID=your-project-id
     FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
     FIREBASE_CLIENT_EMAIL=firebase-adminsdk@...iam.gserviceaccount.com
     ```

4. **Create Pinecone Index** (if not exists)
   - Go to [Pinecone Console](https://www.pinecone.io)
   - Create index named `medico-knowledge`
   - Dimension: `384`
   - Metric: `cosine`

5. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

6. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost/api/v1
   - API Docs: http://localhost/docs

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/google` - Google sign-in
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Chat
- `POST /api/v1/chat` - Send message (streaming SSE)
- `GET /api/v1/chat/sessions` - List chat sessions
- `GET /api/v1/chat/sessions/{id}` - Get session details
- `DELETE /api/v1/chat/sessions/{id}` - Delete session

### Reports
- `POST /api/v1/reports/upload` - Upload medical report
- `GET /api/v1/reports` - List reports
- `GET /api/v1/reports/{id}` - Get report details
- `GET /api/v1/reports/{id}/analysis` - Get AI analysis
- `DELETE /api/v1/reports/{id}` - Delete report

### Users
- `GET /api/v1/users/me` - Get profile with statistics
- `PATCH /api/v1/users/me` - Update profile
- `DELETE /api/v1/users/me` - Delete account

### Health
- `GET /health` - Quick health check
- `GET /api/v1/health/detailed` - Detailed service status

## 🔧 Development

### Running Locally (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
pnpm install
pnpm run dev
```

### Database Migrations

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🛡️ Security Features

✅ **12-Layer Security Implementation**

1. ✅ Firebase JWT Authentication
2. ✅ Role-based Access Control (RBAC)
3. ✅ Rate Limiting (100 req/min per user)
4. ✅ Input Validation (Pydantic schemas)
5. ✅ SQL Injection Prevention (SQLAlchemy ORM)
6. ✅ XSS Protection (CSP headers)
7. ✅ CSRF Protection (SameSite cookies)
8. ✅ File Upload Security (type/size validation)
9. ✅ API Key Protection (environment variables)
10. ✅ HTTPS Ready (nginx SSL termination)
11. ✅ Structured Logging (Loguru)
12. ✅ Error Sanitization (no sensitive data in errors)

## 📊 Tech Stack

### Backend
- **Framework:** FastAPI 0.115.5
- **Database:** PostgreSQL 16 + SQLAlchemy 2.0 (async)
- **Authentication:** Firebase Admin SDK
- **AI/LLM:** Groq (Llama 3.3 70B)
- **Vector DB:** Pinecone
- **OCR:** Tesseract, PyPDF2
- **Embeddings:** sentence-transformers

### Frontend
- **Framework:** Next.js 16
- **UI Library:** React 19
- **Styling:** TailwindCSS 4
- **Components:** shadcn/ui + Radix UI
- **State:** React Hooks
- **Forms:** react-hook-form + Zod

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Reverse Proxy:** Nginx
- **Database:** PostgreSQL 16

## 🌍 Environment Variables

See `.env.example` for complete list. Key variables:

```env
# Required
GROQ_API_KEY=              # Groq AI API key
PINECONE_API_KEY=          # Pinecone vector DB key
FIREBASE_PROJECT_ID=       # Firebase project ID
FIREBASE_PRIVATE_KEY=      # Firebase service account private key
FIREBASE_CLIENT_EMAIL=     # Firebase service account email
SECRET_KEY=                # App secret (32+ chars)
POSTGRES_PASSWORD=         # PostgreSQL password

# Optional
ENVIRONMENT=production     # development/staging/production
LOG_LEVEL=INFO            # DEBUG/INFO/WARNING/ERROR
```

## 📝 Usage

1. **Sign In** - Use Google authentication
2. **Upload Report** - Upload PDF or image of medical report
3. **View Analysis** - Get AI-powered insights and explanations
4. **Ask Questions** - Chat with AI about your health data
5. **Track History** - View all your reports and chat sessions

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Stop existing containers
docker-compose down

# Check for processes
# Windows
netstat -ano | findstr "8000"
netstat -ano | findstr "3000"

# Linux/Mac
lsof -i :8000
lsof -i :3000
```

### Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

### Firebase Authentication Errors
- Verify credentials in `.env`
- Check Firebase console for enabled authentication methods
- Ensure service account has correct permissions

### Pinecone Errors
- Verify API key and environment
- Check index exists with correct dimension (384)
- Ensure index name matches `PINECONE_INDEX_NAME`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Groq](https://groq.com) - Ultra-fast LLM inference
- [Pinecone](https://www.pinecone.io) - Vector database
- [Firebase](https://firebase.google.com) - Authentication
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
- [Next.js](https://nextjs.org) - React framework
- [shadcn/ui](https://ui.shadcn.com) - Beautiful UI components

---

Built with ❤️ for better health understanding
