# NZ Address Validation App

## Overview

This project contains:
- `backend/`: FastAPI API with JWT-protected `/address-check`
- `frontend/`: React app with Cognito Hosted UI login and protected address page
- `docker/Dockerfile`: container image for backend deployment
- `.github/workflows/ci.yml`: CI pipeline for backend tests and frontend build

## Local Setup

### Backend

1. Copy `backend/.env.example` to `backend/.env` and update values.
2. Install packages:
   - `cd backend`
   - `pip install -r requirements.txt`
3. Run API:
   - `uvicorn main:app --reload --port 8000`
4. Health check:
   - `GET http://localhost:8000/health`

### Frontend

1. Copy `frontend/.env.example` to `frontend/.env` and update Cognito/API values.
2. Install packages:
   - `cd frontend`
   - `npm install`
3. Run app:
   - `npm run dev`
4. Open `http://localhost:3000`

## Backend API

### `POST /address-check`

Headers:
- `Authorization: Bearer <JWT>`

Body:
```json
{
  "address": "10 Queen Street, Auckland"
}
```

Success response:
```json
{
  "is_valid": true,
  "normalized_address": "10 Queen Street, Auckland",
  "source": "mock"
}
```

Error codes:
- `400`: invalid input
- `401`: unauthorized or invalid token
- `502`: NZ Post API failure
- `504`: NZ Post timeout

## Testing

Run backend tests:
- `cd backend`
- `pytest -q`

## Deployment Notes

- Build image from repository root:
  - `docker build -f docker/Dockerfile -t nz-address-checker-api .`
- Push to ECR and deploy in ECS/Fargate.
- Configure ALB or API Gateway to route traffic to backend service.
