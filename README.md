# NZ Address Checker Application

A full-stack web application for validating New Zealand addresses built with React and FastAPI.

## 🎯 Overview

The NZ Address Checker is a client-server application that provides:
- **User Authentication**: Login with mock credentials (user123/password123)
- **Address Validation**: Validate addresses against a mock NZ suburb database
- **Modern UI**: Responsive React interface with styled components
- **REST API**: FastAPI backend with automatic Swagger documentation

## 🏗️ Architecture

```
┌─────────────────────────┐
│   Frontend (React)      │
│  - React Router         │
│  - Styled Components    │
│  - Context API          │
│  - Port: 5173           │
└────────────┬────────────┘
             │ HTTP/REST
             │
┌────────────▼────────────┐
│   Backend (FastAPI)     │
│  - Pydantic Models      │
│  - CORS Middleware      │
│  - Mock Services        │
│  - Port: 8000           │
└─────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+

### Installation

1. **Clone or navigate to the project**
   ```bash
   cd "c:\Users\jeffr\OneDrive\Desktop\Jeff\Python\Python Projects\Address-Checker-App"
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📝 Test Credentials
- **Username**: user123
- **Password**: password123

## 🧪 Test Addresses
Try these addresses (they contain valid NZ suburbs):
- Queen Street, Auckland
- Lambton Quay, Wellington
- Colombo Street, Christchurch
- Mount Eden, Auckland
- Ponsonby, Auckland

## 📁 Project Structure

```
address-checker-app/
├── frontend/                 # React SPA (Vite)
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # Auth context
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API client
│   │   ├── styles/          # Global styles
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/              # Static assets
│   ├── package.json
│   ├── vite.config.js
│   └── .env                 # Environment variables
│
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # Pydantic models
│   │   └── config.py        # Configuration
│   ├── requirements.txt
│   └── .env                 # Environment variables
│
├── SETUP.md                 # Setup instructions
├── API.md                   # API documentation
└── README.md                # This file
```

## ✨ Features

### Frontend
- ✓ User authentication with context API
- ✓ Protected routes with redirect
- ✓ Login form with validation
- ✓ Address validation form
- ✓ Real-time result display
- ✓ Error handling and loading states
- ✓ Responsive design
- ✓ localStorage persistence

### Backend
- ✓ REST API with FastAPI
- ✓ CORS middleware configuration
- ✓ Mock authentication service
- ✓ Address validation service
- ✓ Request/response validation with Pydantic
- ✓ Health check endpoint
- ✓ Swagger UI documentation
- ✓ Error handling and logging

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/login` | User authentication |
| POST | `/validate-address` | Address validation |

See [API.md](./API.md) for detailed endpoint documentation.

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **Styled Components** - Component-scoped CSS
- **Fetch API** - HTTP client

### Backend
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **python-dotenv** - Environment variables

## 📚 Documentation

- **[SETUP.md](./SETUP.md)** - Installation and running instructions
- **[API.md](./API.md)** - API endpoint documentation
- **[FOCUSED_DEV_PLAN.md](./FOCUSED_DEV_PLAN.md)** - Detailed development plan

## 🧪 Testing

### Test Login Flow
1. Open http://localhost:5173
2. Enter credentials: user123 / password123
3. Click "Login"
4. Should redirect to address checker

### Test Address Validation
1. Enter an address like "Queen Street, Auckland"
2. Click "Validate Address"
3. Should show validation result

### Test API Directly
Visit http://localhost:8000/docs for interactive Swagger UI to test endpoints.

## 🔧 Available Scripts

### Frontend
```bash
npm run dev      # Start development server (hot reload)
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend
```bash
# Start with auto-reload
python -m uvicorn app.main:app --reload

# Start for production
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# With specific settings
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 🌐 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```env
NZ_POST_API_KEY=mock
DEBUG=True
PORT=8000
HOST=127.0.0.1
```

## ⚠️ Current Limitations

1. **Mock Authentication** - Uses hardcoded credentials (user123/password123)
2. **Mock Address Data** - Uses hardcoded suburb list for validation
3. **No Persistence** - Auth data stored only in browser localStorage
4. **No Database** - All data is ephemeral
5. **Local Development Only** - Not optimized for production

## 🚢 Future Enhancements

- Phase 5: Dockerization
- Phase 6: Infrastructure as Code (Terraform)
- Phase 7: CI/CD Pipeline (GitHub Actions)
- Phase 8: Testing & QA
- Phase 9: Production Deployment

## 🤝 Contributing

Development phases are documented in [FOCUSED_DEV_PLAN.md](./FOCUSED_DEV_PLAN.md).

## 📞 Support

For issues:
1. Check browser console (F12) for client-side errors
2. Check terminal output for server-side errors
3. Visit http://localhost:8000/docs for API reference
4. Review [SETUP.md](./SETUP.md) for troubleshooting

## 📄 License

This project is provided as-is for educational purposes.

## 🎓 Learning Resources

This project demonstrates:
- React with Vite tooling
- React Router for SPA routing
- React Context API for state management
- FastAPI for REST APIs
- Pydantic for data validation
- CORS middleware configuration
- Client-server architecture
- Form handling and validation
- Error handling patterns

---

**Status**: Phase 1-3 Complete ✓  
**Next Phase**: Local Integration Testing (Phase 4)
