# 🎯 ADDRESS CHECKER APP - FOCUSED DEVELOPMENT PLAN
## Phases 1-4: Frontend, Backend, Local Integration

---

## 📌 PROJECT SCOPE (THIS PLAN)

### ✅ Included in This Plan
- **Phase 1:** Project setup & Git initialization
- **Phase 2:** Frontend React SPA (React + Vite + Styled-components)
- **Phase 3:** Backend FastAPI (2 endpoints, mocked auth & validation)
- **Phase 4:** Local integration & end-to-end testing

### ⏸️ Deferred (Later Phases)
- Dockerization (Phase 5)
- Infrastructure as Code (Phase 6)
- CI/CD Pipeline (Phase 7)
- Testing & QA (Phase 8)
- Production Deployment (Phase 9)
- Optimization (Phase 10)

---

## 🏗️ TECHNICAL DECISIONS

| Layer | Technology | Reason |
|-------|-----------|--------|
| **Frontend** | React 18 + Vite | Fast builds, modern tooling |
| **State Mgmt** | React Context API | Simple, no dependencies |
| **Styling** | Styled-components | Component-scoped CSS |
| **Routing** | React Router v6 | Standard for SPAs |
| **HTTP Client** | Fetch API | No external dependency |
| **Backend** | FastAPI | Async, auto-docs, fast |
| **Validation** | Pydantic | Built-in, typed models |
| **Address Mock** | Separate module | Easy swap to real API |
| **Auth Mock** | Hardcoded credentials | Simple, clear for demo |
| **Local Dev** | Vite dev server + Uvicorn | Fast refresh, simple setup |

---

## 📂 PROJECT STRUCTURE (FINAL)

```
address-checker-app/
│
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── README.md                      # Project overview
│
├── frontend/                      # React SPA
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.jsx          # Login form component
│   │   │   ├── AddressChecker.jsx # Address validation form
│   │   │   └── ProtectedRoute.jsx # Route protection HOC
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # Auth state context
│   │   ├── hooks/
│   │   │   ├── useAuth.js         # Auth hook
│   │   │   └── useApi.js          # API call hook
│   │   ├── services/
│   │   │   └── apiClient.js       # Fetch wrapper
│   │   ├── styles/
│   │   │   └── GlobalStyles.js    # Styled-components theme
│   │   ├── App.jsx                # Main component
│   │   └── index.jsx              # Entry point
│   ├── public/
│   │   └── index.html             # HTML template
│   ├── package.json               # Dependencies
│   ├── vite.config.js             # Vite config
│   └── .env.example               # Environment template
│
├── backend/                       # FastAPI backend
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py            # Login endpoint
│   │   │   └── address.py         # Validation endpoint
│   │   ├── services/
│   │   │   ├── nz_post_mock.py    # Mock NZ Post service
│   │   │   └── nz_post_real.py    # Real NZ Post (future)
│   │   ├── main.py                # FastAPI app
│   │   ├── models.py              # Pydantic models
│   │   └── config.py              # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template
│   └── __init__.py                # Package init
│
└── docs/
    ├── API.md                     # API documentation
    └── SETUP.md                   # Setup instructions
```

---

## 🔧 PHASE 1: PROJECT SETUP
**Duration:** 1 day | **Owner:** DevOps Engineer

### 1.1 Git Repository Initialization
- [ ] Initialize Git repository: `git init`
- [ ] Create `.gitignore` with:
  - `node_modules/`
  - `__pycache__/`
  - `*.pyc`
  - `.env`
  - `.venv/`
  - `dist/`
  - `build/`
  - `.DS_Store`
- [ ] Create initial commit: `git add . && git commit -m "Initial project structure"`
- [ ] (Optional) Push to GitHub

### 1.2 Frontend Initialization
- [ ] Create `frontend/` directory
- [ ] Initialize Node.js project: `npm init -y`
- [ ] Install Vite: `npm install --save-dev vite @vitejs/plugin-react`
- [ ] Install React: `npm install react react-dom react-router-dom`
- [ ] Install Styled-components: `npm install styled-components`
- [ ] Create `vite.config.js` with React plugin
- [ ] Create `public/index.html` template
- [ ] Create `src/` directory structure

### 1.3 Backend Initialization
- [ ] Create `backend/` directory
- [ ] Create Python virtual environment: `python -m venv venv`
- [ ] Activate venv: `venv\Scripts\activate` (Windows)
- [ ] Install FastAPI: `pip install fastapi uvicorn`
- [ ] Install Pydantic: `pip install pydantic`
- [ ] Install python-dotenv: `pip install python-dotenv`
- [ ] Create `requirements.txt`: `pip freeze > requirements.txt`
- [ ] Create `app/` directory structure

### 1.4 Environment Setup
- [ ] Create `frontend/.env.example`:
  ```env
  VITE_API_URL=http://localhost:8000
  ```
- [ ] Create `backend/.env.example`:
  ```env
  NZ_POST_API_KEY=your_key_here
  DEBUG=True
  PORT=8000
  HOST=127.0.0.1
  ```

**Deliverable:** Project initialized with all directories and dependencies

---

## 🎨 PHASE 2: FRONTEND DEVELOPMENT
**Duration:** 5 days | **Owner:** Frontend Engineer

### 2.1 Core Setup
- [ ] Create `src/App.jsx` - Main component with router
- [ ] Create `src/index.jsx` - React entry point
- [ ] Configure Vite with React plugin
- [ ] Setup package.json scripts:
  - `npm run dev` → Vite dev server
  - `npm run build` → Build for production
  - `npm run preview` → Preview build

### 2.2 Authentication Context
**File:** `src/context/AuthContext.jsx`
- [ ] Create Context with:
  - `isAuthenticated` - boolean
  - `user` - current user object
  - `login()` - login function
  - `logout()` - logout function
- [ ] Implement localStorage persistence
- [ ] Export context and provider

### 2.3 Custom Hooks
**File:** `src/hooks/useAuth.js`
- [ ] Use AuthContext
- [ ] Return: `{ isAuthenticated, user, login, logout }`

**File:** `src/hooks/useApi.js`
- [ ] Accept endpoint and method
- [ ] Return: `{ data, error, loading, execute }`

### 2.4 API Client Service
**File:** `src/services/apiClient.js`
- [ ] Base URL from env variable
- [ ] Helper function for GET/POST/PUT/DELETE
- [ ] Handle errors gracefully
- [ ] Add request/response logging

### 2.5 Global Styling
**File:** `src/styles/GlobalStyles.js`
- [ ] Create styled-components theme:
  - Colors (primary, secondary, error, success)
  - Fonts and sizes
  - Spacing scale
  - Breakpoints for responsive
- [ ] Create global styles (reset, base elements)

### 2.6 Login Component
**File:** `src/components/Login.jsx`
- [ ] Form with:
  - Username input field
  - Password input field
  - Submit button
  - Error message display
- [ ] Styling with styled-components
- [ ] State management:
  - username (controlled input)
  - password (controlled input)
  - error (error state)
  - loading (submit state)
- [ ] On submit:
  - Validate fields not empty
  - Call POST /login
  - If success: redirect to /address-checker
  - If error: display error message
- [ ] Password field should mask input

### 2.7 Address Checker Component
**File:** `src/components/AddressChecker.jsx`
- [ ] Form with:
  - Address input field (textarea or input)
  - Validate button
  - Result display area
- [ ] State management:
  - address (controlled input)
  - result (validation result)
  - error (error state)
  - loading (request state)
- [ ] On submit:
  - Validate address not empty
  - Call POST /validate-address
  - Display result (valid/invalid)
  - Handle errors
- [ ] Display address and validation status

### 2.8 Protected Route Component
**File:** `src/components/ProtectedRoute.jsx`
- [ ] Check if user is authenticated
- [ ] If yes: render component
- [ ] If no: redirect to /login

### 2.9 App Router Setup
**File:** `src/App.jsx`
- [ ] Setup routes:
  - `/login` → Login component
  - `/address-checker` → AddressChecker component (protected)
  - `/` → Redirect to /address-checker if authenticated, else /login
- [ ] Wrap with AuthProvider
- [ ] Setup navigation/navbar

### 2.10 Testing & Validation
- [ ] Test form inputs work
- [ ] Test form validation (empty field checks)
- [ ] Test UI responsiveness (mobile/tablet/desktop)
- [ ] Test styling consistency
- [ ] Verify no console errors

**Deliverable:** Complete React SPA UI (no backend yet)

---

## ⚙️ PHASE 3: BACKEND DEVELOPMENT
**Duration:** 5 days | **Owner:** Backend Engineer

### 3.1 FastAPI App Setup
**File:** `backend/app/main.py`
- [ ] Create FastAPI app instance
- [ ] Setup CORS middleware:
  - Allow localhost:3000 (frontend)
  - Allow * for testing (restrict in production)
- [ ] Setup request/response logging
- [ ] Create health check endpoint: `GET /health`

### 3.2 Pydantic Models
**File:** `backend/app/models.py`
- [ ] `LoginRequest` model:
  - username: str (required, min 1)
  - password: str (required, min 1)
- [ ] `LoginResponse` model:
  - message: str
- [ ] `AddressValidationRequest` model:
  - address: str (required, min 3)
- [ ] `AddressValidationResponse` model:
  - status: "valid" | "invalid"
  - address: str
  - message: str (optional, for errors)

### 3.3 Configuration
**File:** `backend/app/config.py`
- [ ] Load environment variables
- [ ] Mock credentials: username="user123", password="password123"
- [ ] Debug mode from env
- [ ] Port and host from env

### 3.4 Mock Address Validation Service
**File:** `backend/app/services/nz_post_mock.py`
- [ ] Function `validate_address(address: str) -> dict`
- [ ] Simple validation logic:
  - Check if address contains NZ suburb/city names
  - Return valid for recognized addresses
  - Return invalid for unrecognized
- [ ] Mock database of NZ addresses/suburbs:
  ```python
  VALID_SUBURBS = [
      "Auckland", "Wellington", "Christchurch", 
      "Hamilton", "Tauranga", "Dunedin",
      "Queen Street", "Lambton Quay", "Colombo Street"
  ]
  ```

### 3.5 Real Address Validation Service (Template)
**File:** `backend/app/services/nz_post_real.py`
- [ ] Function `validate_address(address: str) -> dict`
- [ ] Template for NZ Post API integration:
  ```python
  # TODO: Implement with real NZ Post API
  # Requires: NZ_POST_API_KEY from .env
  # Endpoint: https://api.nzpost.co.nz/...
  # Method: POST with address
  # Response: Parse and return valid/invalid
  ```
- [ ] Leave as TODO for later

### 3.6 Login Endpoint
**File:** `backend/app/routes/auth.py`
- [ ] Endpoint: `POST /login`
- [ ] Request: `LoginRequest` (username, password)
- [ ] Response: `LoginResponse` (message) on success
- [ ] Logic:
  - Check username == "user123" and password == "password123"
  - If match: return 200 with success message
  - If not match: return 401 with error message
- [ ] Error handling:
  - 400: Invalid request body
  - 401: Invalid credentials

### 3.7 Address Validation Endpoint
**File:** `backend/app/routes/address.py`
- [ ] Endpoint: `POST /validate-address`
- [ ] Request: `AddressValidationRequest` (address)
- [ ] Response: `AddressValidationResponse` (status, address)
- [ ] Logic:
  - Call mock validation service
  - Return validation result
- [ ] Error handling:
  - 400: Invalid request body
  - 500: Service error

### 3.8 FastAPI App Integration
**File:** `backend/app/main.py` (continued)
- [ ] Import routes
- [ ] Include auth routes: `app.include_router(auth.router)`
- [ ] Include address routes: `app.include_router(address.router)`
- [ ] Verify auto-generated docs at `/docs`

### 3.9 Run and Test
- [ ] Start Uvicorn: `python -m uvicorn app.main:app --reload`
- [ ] Test endpoints manually:
  - `GET http://localhost:8000/health`
  - `POST http://localhost:8000/login` (correct credentials)
  - `POST http://localhost:8000/login` (wrong credentials)
  - `POST http://localhost:8000/validate-address`
- [ ] Check Swagger UI: `http://localhost:8000/docs`

**Deliverable:** Complete FastAPI backend with endpoints working

---

## 🔄 PHASE 4: LOCAL INTEGRATION
**Duration:** 3 days | **Owner:** Full Stack

### 4.1 Frontend API Integration - Login
- [ ] Update `Login.jsx` to call real backend
- [ ] Implement login flow:
  1. User fills form
  2. Click submit
  3. POST to `http://localhost:8000/login`
  4. If success: store in AuthContext, redirect
  5. If error: display error message

### 4.2 Frontend API Integration - Address Validation
- [ ] Update `AddressChecker.jsx` to call real backend
- [ ] Implement validation flow:
  1. User enters address
  2. Click validate
  3. POST to `http://localhost:8000/validate-address`
  4. Display result (valid/invalid)
  5. Handle errors

### 4.3 Update API Client
**File:** `frontend/src/services/apiClient.js`
- [ ] Set base URL from `VITE_API_URL`
- [ ] Add proper error handling
- [ ] Add request/response logging

### 4.4 Environment Variables
- [ ] Create `frontend/.env` from `.env.example`
- [ ] Set: `VITE_API_URL=http://localhost:8000`
- [ ] Create `backend/.env` from `.env.example`
- [ ] Set: `NZ_POST_API_KEY=mock`, `DEBUG=True`

### 4.5 Start Both Services
- [ ] Terminal 1: `cd frontend && npm run dev`
  - Frontend runs on http://localhost:5173
- [ ] Terminal 2: `cd backend && python -m uvicorn app.main:app --reload`
  - Backend runs on http://localhost:8000

### 4.6 End-to-End Testing
- [ ] Test full login flow:
  1. Open http://localhost:5173
  2. See login form
  3. Enter: user123 / password123
  4. Click login
  5. Should redirect to address checker
  6. Check no errors in console
  
- [ ] Test address validation:
  1. Enter: "Queen Street, Auckland"
  2. Click validate
  3. Should show result
  4. Check response from backend
  
- [ ] Test error cases:
  1. Wrong login (should show error)
  2. Empty form (should validate)
  3. Invalid address (should show invalid)

### 4.7 Browser DevTools Verification
- [ ] Open DevTools (F12)
- [ ] Network tab: Verify requests to localhost:8000
- [ ] Console tab: Check for errors
- [ ] Application tab: Check localStorage for auth

### 4.8 Documentation
- [ ] Create `docs/SETUP.md`:
  - How to install frontend
  - How to install backend
  - How to run both locally
  - Environment variables needed
  - Testing endpoints
  
- [ ] Create `docs/API.md`:
  - Endpoint documentation
  - Request/response examples
  - Error codes

**Deliverable:** Full working application locally

---

## ✅ SUCCESS CRITERIA

| Phase | Success Criteria |
|-------|------------------|
| **Phase 1** | ✓ Git initialized, directories created, dependencies installed |
| **Phase 2** | ✓ React SPA loads, forms functional, styling complete, UI responsive |
| **Phase 3** | ✓ Backend running, endpoints responding, mock data working |
| **Phase 4** | ✓ Frontend and backend connected, full flow working end-to-end |

---

## ⚡ QUICK REFERENCE COMMANDS

### Frontend
```bash
cd frontend
npm install
npm run dev              # Starts on http://localhost:5173
npm run build            # Creates production build
```

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
python -m uvicorn app.main:app --reload  # Starts on http://localhost:8000
```

### Test Credentials
```
Username: user123
Password: password123
```

### Test Addresses
```
Queen Street, Auckland        → Valid
Lambton Quay, Wellington      → Valid
Some Invalid Address 123      → Invalid
```

---

## 📝 TASK CHECKLIST

**Phase 1:**
- [ ] Git initialized
- [ ] Frontend structure created
- [ ] Backend structure created
- [ ] Dependencies installed
- [ ] Environment templates created

**Phase 2:**
- [ ] AuthContext created
- [ ] Custom hooks created
- [ ] API client created
- [ ] Global styles created
- [ ] Login component created
- [ ] AddressChecker component created
- [ ] ProtectedRoute created
- [ ] Router setup
- [ ] UI tested locally

**Phase 3:**
- [ ] FastAPI app created
- [ ] Pydantic models created
- [ ] Config file created
- [ ] Mock validation service created
- [ ] Auth endpoint created
- [ ] Address endpoint created
- [ ] CORS middleware configured
- [ ] Endpoints tested with curl/Postman

**Phase 4:**
- [ ] Frontend connected to backend
- [ ] Login flow tested end-to-end
- [ ] Address validation flow tested
- [ ] Error handling tested
- [ ] Documentation created

---

## 🎯 NEXT ACTIONS (AFTER THIS PHASE)

Once Phase 4 is complete, next phases are:
1. **Phase 5:** Dockerization
2. **Phase 6:** Infrastructure as Code (Terraform)
3. **Phase 7:** CI/CD Pipeline (GitHub Actions)
4. **Phase 8:** Testing & QA
5. **Phase 9:** Production Deployment

---

## 📊 RESOURCES

- **Frontend:** 1 engineer, 5 days
- **Backend:** 1 engineer, 5 days
- **Integration:** 1 engineer, 3 days
- **Total:** ~2 weeks for Phases 1-4

---

## ⚠️ KEY DECISIONS

1. **Mock Authentication:** Simple hardcoded credentials for now
   - Later: Replace with AWS Cognito
   
2. **Mock Address Validation:** Simple suburb matching
   - Later: Replace with real NZ Post API (separate file ready)
   
3. **Local Development:** Vite dev server + Uvicorn
   - Later: Switch to Docker for consistency
   
4. **State Management:** React Context API (simple)
   - Later: Could upgrade to Redux if needed
   
5. **Styling:** Styled-components (component-scoped)
   - Later: Could add Tailwind if preferred

---

**Status:** Ready to implement
**Start Date:** When you're ready
**Estimated Completion:** 2 weeks (Phases 1-4)

