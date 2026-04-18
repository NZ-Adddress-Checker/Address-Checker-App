# NZ Address Checker - Setup Instructions

## Project Overview
Full-stack application for validating New Zealand addresses with:
- **Frontend**: React 18 + Vite + Styled Components
- **Backend**: FastAPI + Pydantic with mock NZ Post service
- **Architecture**: Client-server with JWT-like auth context

## Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- pip (Python package manager)

## Phase 1-3: Project Structure ✓ COMPLETE
The project has been initialized with all directories and files created.

```
address-checker-app/
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── components/        # UI Components
│   │   ├── context/           # Auth Context
│   │   ├── hooks/             # Custom hooks
│   │   ├── services/          # API client
│   │   ├── styles/            # Global styles
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env                   # Environment variables
│
├── backend/                   # FastAPI server
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── main.py
│   │   ├── models.py
│   │   └── config.py
│   ├── requirements.txt
│   └── .env                   # Environment variables
│
└── .gitignore
```

## Installation & Running

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: http://localhost:8000
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:5173 (or as shown in terminal)

## Test Credentials
```
Username: user123
Password: password123
```

## Test Addresses (Valid)
```
Queen Street, Auckland
Lambton Quay, Wellington
Colombo Street, Christchurch
Mount Eden, Auckland
Ponsonby, Auckland
```

## API Endpoints

### Authentication
- **POST** `/login`
  - Request: `{ "username": "user123", "password": "password123" }`
  - Response: `{ "message": "Login successful" }`
  - Errors: 401 Unauthorized for invalid credentials

### Address Validation
- **POST** `/validate-address`
  - Request: `{ "address": "Queen Street, Auckland" }`
  - Response: `{ "status": "valid", "address": "...", "message": "..." }`
  - Errors: 400 Bad Request, 500 Internal Server Error

### Health Check
- **GET** `/health`
  - Response: `{ "status": "healthy", "message": "Service is running" }`

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
NZ_POST_API_KEY=mock
DEBUG=True
PORT=8000
HOST=127.0.0.1
```

## Features Implemented

### Frontend (Phase 2)
- ✓ React Router with protected routes
- ✓ AuthContext with localStorage persistence
- ✓ useAuth and useApi custom hooks
- ✓ API client service with error handling
- ✓ Login component with validation
- ✓ Address checker component
- ✓ Global styling with Styled Components
- ✓ Responsive UI design

### Backend (Phase 3)
- ✓ FastAPI with CORS middleware
- ✓ Pydantic models for type safety
- ✓ Authentication endpoint (/login)
- ✓ Address validation endpoint (/validate-address)
- ✓ Mock NZ Post service with suburb list
- ✓ Configuration management
- ✓ Health check endpoint
- ✓ Swagger documentation (/docs)

### Integration (Phase 4)
- ✓ Environment templates created
- ✓ API client configured
- ✓ Error handling implemented
- ✓ End-to-end flow ready

## End-to-End Testing

1. **Start Backend**: 
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Test Login**:
   - Navigate to http://localhost:5173
   - Enter username: `user123`
   - Enter password: `password123`
   - Click Login
   - Should redirect to address checker

4. **Test Address Validation**:
   - Enter an address containing a NZ suburb
   - Click "Validate Address"
   - Should display validation result

## Build for Production

### Frontend
```bash
cd frontend
npm run build
npm run preview
```

### Backend
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Frontend won't start
- Check Node.js version: `node --version` (should be 16+)
- Delete node_modules and package-lock.json, then `npm install` again

### Backend won't start
- Check Python version: `python --version` (should be 3.9+)
- Check requirements are installed: `pip list | grep fastapi`
- Check port 8000 is not in use

### CORS errors
- Ensure backend is running on http://localhost:8000
- Check VITE_API_URL in frontend .env

### Authentication fails
- Verify credentials: username=user123, password=password123
- Check browser console for errors
- Check backend logs

## Next Steps

After Phase 4 local testing:
- Phase 5: Docker containerization
- Phase 6: Infrastructure as Code
- Phase 7: CI/CD Pipeline
- Phase 8: Testing & QA
- Phase 9: Production Deployment

## Support

For issues or questions:
1. Check the FOCUSED_DEV_PLAN.md for detailed requirements
2. Review browser console (F12) for client-side errors
3. Check backend server logs for server-side errors
4. Visit FastAPI docs at http://localhost:8000/docs for API reference
