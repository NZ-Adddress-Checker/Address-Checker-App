# NZ Address Checker

A secure, production-ready NZ address validation application using FastAPI backend, React frontend with AWS Cognito authentication, and Docker orchestration.

## Project Structure

```
├── backend/              # FastAPI API with address validation
├── frontend/             # React app with Cognito OAuth2 PKCE flow
├── docker/               # Docker & orchestration files
├── docs/                 # Setup guides and documentation
└── README.md             # This file
```

## Features

- ✅ AWS Cognito OAuth2 authentication with PKCE flow
- ✅ JWT token validation (RS256)
- ✅ NZ address validation against official database
- ✅ Docker Compose orchestration
- ✅ Environment-driven configuration
- ✅ Health check endpoints for monitoring

## Architecture

| Component | Technology | Port |
|-----------|-----------|------|
| Backend API | FastAPI (Python 3.12) | 8000 |
| Frontend App | React + Vite (Node 20) | 5173 (local) / 8080 (Docker) |
| Web Server | Nginx 1.27-alpine | N/A |
| Auth | AWS Cognito | Hosted UI |

## Prerequisites

- **Python** 3.12+ (for local backend development)
- **Node.js** 20+ (for local frontend development)
- **Docker Desktop** (for containerized workflow)
- **AWS Account** with Cognito (for authentication)

## Quick Start: Docker (Recommended)

### 1. Setup Cognito

Follow the comprehensive [Cognito Setup Guide](docs/COGNITO_SETUP_GUIDE.md) to:
- Create User Pool and App Client
- Configure OAuth scopes and callback URLs
- Note your Client ID and Domain URL

### 2. Configure Environment

Copy and edit docker environment file:
```bash
cp docker/.env.example docker/.env
```

Update with your Cognito values:
```env
VITE_COGNITO_DOMAIN=https://your-domain.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
VITE_COGNITO_SCOPE=email+openid+phone+profile
```

### 3. Run Application

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

### 4. Access Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Health Check**: 
  - Backend: `curl http://localhost:8000/health`
  - Frontend: `curl http://localhost:8080/health`

### 5. Stop Application

```bash
docker compose -f docker/docker-compose.yml down
```

## Local Development

### Backend Setup

1. Create virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate  # Windows
   source .venv/bin/activate # macOS/Linux
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your Cognito credentials
   ```

4. Run development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. Backend available at: http://localhost:8000

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your Cognito credentials
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Frontend available at: http://localhost:5173

## Environment Configuration

### Backend (.env)

```env
# API Configuration
ENV=dev  # or 'prod'
API_PORT=8000

# CORS
FRONTEND_ORIGIN=http://localhost:5173

# JWT / Cognito
JWT_ISSUER=https://cognito-idp.ap-southeast-2.amazonaws.com/user-pool-id
JWT_AUDIENCE=client-id
JWKS_URL=https://cognito-idp.ap-southeast-2.amazonaws.com/user-pool-id/.well-known/jwks.json
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_COGNITO_DOMAIN=https://your-domain.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_SCOPE=email+openid+phone+profile
```

### Docker (docker/.env)

```env
VITE_COGNITO_DOMAIN=https://your-domain.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
VITE_COGNITO_SCOPE=email+openid+phone+profile
```

## API Endpoints

### Public Endpoints

```
GET /health
Response: {"status":"ok","env":"dev"}
```

### Protected Endpoints (JWT Required)

**Get Address Suggestions**
```
GET /address-suggestions?query=<search-term>
Header: Authorization: Bearer <jwt-token>
Response:
[
  {"address":"10 Queen Street, Auckland 1010"},
  {"address":"10 Queen Street, Wellington 6011"}
]
```

**Validate Address**
```
POST /address-check
Header: Authorization: Bearer <jwt-token>
Body: {"address":"10 Queen Street, Auckland"}
Response:
{
  "is_valid": true,
  "normalized_address": "10 Queen Street, Auckland 1010",
  "source": "mock"
}
```

## Health Checks

Monitor application health:

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health (Docker)
curl http://localhost:8080/health
```

Expected responses:
- Backend: `{"status":"ok","env":"dev"}`
- Frontend: `ok`

## Troubleshooting

### Docker Issues

**Containers won't start**
```bash
# Check logs
docker compose -f docker/docker-compose.yml logs

# Restart with fresh build
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d --build
```

**Port already in use**
```bash
# Change ports in docker-compose.yml or stop conflicting services
docker ps  # Show running containers
docker stop <container-name>
```

### Authentication Issues

**"Cognito is not configured"**
- Verify all `VITE_COGNITO_*` variables are set in `.env` file
- Check that values match your Cognito app client settings
- Restart frontend: `npm run dev` (local) or rebuild Docker image

**"Invalid redirect URI"**
- Ensure callback URL in your environment matches Cognito app client settings
- For Docker: `http://localhost:8080/callback`
- For local dev: `http://localhost:5173/callback`

**"User not found" or authentication fails**
- Verify user exists in Cognito User Pool
- Check that user is in CONFIRMED state (not FORCE_CHANGE_PASSWORD)
- Try signing out and logging back in

### Backend Issues

**503 Service Unavailable**
- Likely JWKS endpoint unreachable (network/firewall issue)
- Check internet connectivity
- Verify `JWT_ISSUER` and `JWKS_URL` are correct

**401 Invalid Token**
- Token may have expired (default 1 hour)
- Request new token by logging in again
- Verify `JWT_AUDIENCE` matches your Cognito Client ID

### Frontend Issues

**Page won't load**
- Check browser console for errors: F12 → Console tab
- Verify backend is running: `curl http://localhost:8000/health`
- Clear browser cache: Ctrl+Shift+Delete

**API requests failing**
- Check `VITE_API_BASE_URL` points to correct backend
- Verify CORS is enabled (check backend logs)
- Confirm token is valid (check Application tab → Storage → Tokens)

## Development Tips

### Local Multi-Terminal Workflow

**Terminal 1 - Backend:**
```bash
.\.venv\Scripts\Activate
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then access frontend at http://localhost:5173

### Docker Development Workflow

```bash
# Build and start
docker compose -f docker/docker-compose.yml up -d --build

# View logs
docker compose -f docker/docker-compose.yml logs -f

# Make changes to code, rebuild and restart
docker compose -f docker/docker-compose.yml restart frontend
```

### Environment Validation

Check that all required variables are set:

```bash
# Backend
echo $JWT_ISSUER
echo $VITE_COGNITO_CLIENT_ID

# Frontend
echo $VITE_COGNITO_DOMAIN
echo $VITE_COGNITO_REDIRECT_URI
```

## Deployment

### Production Checklist

- [ ] All `VITE_*` and `JWT_*` variables configured
- [ ] Cognito callback URLs use HTTPS
- [ ] JWT tokens use RS256 (public key verification)
- [ ] CORS only allows your domain
- [ ] Environment set to `prod` not `dev`
- [ ] Docker images pushed to registry
- [ ] Health checks configured for monitoring

### Cloud Deployment Options

1. **AWS ECS**: Deploy Docker images
2. **Vercel**: Deploy frontend (React app)
3. **Heroku**: Deploy backend (FastAPI app)
4. **DigitalOcean**: Docker Compose on droplet
5. **Kubernetes**: Use Docker images with K8s manifests

## Documentation

- [Cognito Setup Guide](docs/COGNITO_SETUP_GUIDE.md) - Complete AWS Cognito configuration
- API docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

## License

This project is provided as-is for evaluation and use. See LICENSE file for details.

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Review [Cognito Setup Guide](docs/COGNITO_SETUP_GUIDE.md)
3. Check application logs: `docker compose logs -f`
4. Review browser console: F12 → Console tab
