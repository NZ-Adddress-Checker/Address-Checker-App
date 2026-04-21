# NZ Address Checker

A full-stack NZ address validation application — FastAPI backend, React frontend with AWS Cognito OAuth2 PKCE authentication, and Docker orchestration.

## Project Structure

```
├── backend/              # FastAPI API with JWT auth and address validation
├── frontend/             # React + Vite app with Cognito PKCE flow
├── docker/               # Dockerfiles and docker-compose
├── .github/workflows/    # CI/CD GitHub Actions pipelines
└── README.md
```

## Architecture

| Component | Technology | Port |
|-----------|-----------|------|
| Backend API | FastAPI (Python 3.12) | 8000 |
| Frontend | React + Vite (Node 20) | 5173 (local) / 8080 (Docker) |
| Web Server | Nginx 1.27-alpine | 8080 (Docker) |
| Auth | AWS Cognito (Hosted UI) | — |

## Prerequisites

- **Python** 3.12+
- **Node.js** 20+
- **Docker Desktop** (for containerised workflow)
- **AWS Account** with a Cognito User Pool

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate   # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
cp .env.example .env       # then fill in your values
uvicorn main:app --reload --port 8000
```

Backend available at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
cp .env.example .env       # then fill in your values
npm run dev
```

Frontend available at http://localhost:5173

---

## Docker

```bash
# Start
docker compose -f docker/docker-compose.yml up -d --build

# Stop
docker compose -f docker/docker-compose.yml down

# Logs
docker compose -f docker/docker-compose.yml logs -f
```

- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- Health: `curl http://localhost:8000/health`

For Docker, set the Cognito environment variables as shell exports or in a `.env` file alongside `docker-compose.yml` before running `up`.

---

## Environment Variables

### Backend — `backend/.env` (copy from `backend/.env.example`)

| Variable | Description |
|---|---|
| `APP_ENV` | `dev` or `prod` |
| `FRONTEND_ORIGINS` | Comma-separated allowed origins, e.g. `http://localhost:5173` |
| `JWT_ISSUER` | Cognito issuer URL |
| `JWT_AUDIENCE` | Cognito app client ID |
| `JWKS_URL` | Cognito JWKS endpoint |
| `NZPOST_MOCK` | `true` to use mock data, `false` for real NZ Post API |
| `NZPOST_API_URL` | NZ Post API endpoint (only needed when mock is false) |
| `NZPOST_API_KEY` | NZ Post API key (only needed when mock is false) |

### Frontend — `frontend/.env` (copy from `frontend/.env.example`)

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Backend URL, e.g. `http://localhost:8000` |
| `VITE_COGNITO_DOMAIN` | Cognito hosted UI domain URL |
| `VITE_COGNITO_CLIENT_ID` | Cognito app client ID |
| `VITE_COGNITO_REDIRECT_URI` | Must match callback URL registered in Cognito |
| `VITE_COGNITO_SCOPE` | e.g. `email+openid+phone` |

---

## API Endpoints

### Public

```
GET /health
→ {"status": "ok", "env": "dev"}
```

### Protected (requires `Authorization: Bearer <id_token>`)

```
GET /address-suggestions
→ {"items": ["10 Queen Street, Auckland 1010", ...]}

POST /address-check
Body: {"address": "10 Queen Street, Auckland"}
→ {"is_valid": true, "normalized_address": "10 Queen Street, Auckland", "source": "mock"}
```

---

## Troubleshooting

**"Cognito is not configured"** — All four `VITE_COGNITO_*` variables must be set in `frontend/.env`.

**401 Unauthorized** — Token is missing, expired, or `JWT_AUDIENCE` / `JWT_ISSUER` in `backend/.env` does not match your Cognito pool.

**Containers won't start** — Run `docker compose -f docker/docker-compose.yml logs` to inspect errors.

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
