# NZ Address Validation App

## Overview

This repository contains:
- backend: FastAPI API with JWT-protected address endpoints.
- frontend: React application with Cognito Hosted UI and PKCE login flow.
- docker: Backend and frontend container definitions, nginx config, and compose stack.

Current architecture uses these API endpoints:
- GET /health
- GET /address-suggestions (JWT required)
- POST /address-check (JWT required)

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker Desktop (optional for container workflow)

## Local Development

### 1. Backend setup

1. Copy backend/.env.example to backend/.env and fill real Cognito/NZ Post values as needed.
2. Install dependencies:
   - cd backend
   - pip install -r requirements.txt
3. Run API:
   - uvicorn main:app --reload --port 8000
4. Health check:
   - http://localhost:8000/health

### 2. Frontend setup

1. Copy frontend/.env.example to frontend/.env and update values.
2. Install dependencies:
   - cd frontend
   - npm install
3. Start Vite:
   - npm run dev
4. Open:
   - http://localhost:5173

## Docker Workflow

All Docker-related files are under the docker folder.

### Run full stack (backend + frontend)

From repository root:
- docker compose -f docker/docker-compose.yml up -d --build

Service URLs:
- Backend API: http://localhost:8000
- Frontend app: http://localhost:8080
- Frontend health: http://localhost:8080/health

### Stop stack

- docker compose -f docker/docker-compose.yml down

### Optional compose environment overrides

If you want to override frontend build-time variables, copy docker/.env.example to docker/.env and export those values in your shell before running compose.

## API Contract (address-check)

Request body:
{
  "address": "10 Queen Street, Auckland"
}

Response shape:
{
  "is_valid": true,
  "normalized_address": "10 Queen Street, Auckland 1010",
  "source": "mock"
}

Common error codes:
- 400 invalid input
- 401 missing/invalid/expired token
- 503 temporary JWKS validation outage
- 502 upstream NZ Post error
- 504 upstream timeout
