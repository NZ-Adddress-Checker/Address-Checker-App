# NZ Address Checker - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
The application uses mock authentication with hardcoded credentials.
- Username: `user123`
- Password: `password123`

Credentials are validated on the `/login` endpoint. Success stores user in browser localStorage.

## Endpoints

### 1. Health Check
Check if the API is running.

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

---

### 2. Login
Authenticate a user with username and password.

**Endpoint**: `POST /login`

**Request Body**:
```json
{
  "username": "user123",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful"
}
```

**Error Response** (401 Unauthorized):
```json
{
  "detail": "Invalid credentials"
}
```

**Example cURL**:
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}'
```

---

### 3. Validate Address
Validate a New Zealand address against a mock suburb list.

**Endpoint**: `POST /validate-address`

**Request Body**:
```json
{
  "address": "Queen Street, Auckland"
}
```

**Response** (200 OK) - Valid Address:
```json
{
  "status": "valid",
  "address": "Queen Street, Auckland",
  "message": "Address contains valid suburb: Queen Street"
}
```

**Response** (200 OK) - Invalid Address:
```json
{
  "status": "invalid",
  "address": "Some random address",
  "message": "Address does not contain a recognized NZ suburb"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Invalid request"
}
```

**Example cURL**:
```bash
curl -X POST http://localhost:8000/validate-address \
  -H "Content-Type: application/json" \
  -d '{"address":"Queen Street, Auckland"}'
```

---

## Valid Suburbs (Mock Data)

The mock validation service recognizes these NZ suburbs/locations:
- Auckland
- Wellington
- Christchurch
- Hamilton
- Tauranga
- Dunedin
- Queen Street
- Lambton Quay
- Colombo Street
- Ponsonby
- Mount Eden
- Parnell
- Takapuna
- Grey Lynn
- Balmoral
- Te Aro
- Karori
- Northland
- Manukau
- Waitakere

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request format or missing required fields |
| 401 | Unauthorized | Invalid credentials or authentication failed |
| 500 | Internal Server Error | Server-side error occurred |

---

## CORS Headers

The API includes CORS middleware that allows:
- **Allow-Origin**: `*` (all origins in dev, restrict in production)
- **Allow-Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allow-Headers**: Content-Type, Authorization

---

## Request/Response Examples

### Example 1: Successful Login
```bash
$ curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}'

Response:
{
  "message": "Login successful"
}
```

### Example 2: Failed Login
```bash
$ curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"wrong"}'

Response (401):
{
  "detail": "Invalid credentials"
}
```

### Example 3: Valid Address
```bash
$ curl -X POST http://localhost:8000/validate-address \
  -H "Content-Type: application/json" \
  -d '{"address":"Lambton Quay, Wellington"}'

Response:
{
  "status": "valid",
  "address": "Lambton Quay, Wellington",
  "message": "Address contains valid suburb: Lambton Quay"
}
```

### Example 4: Invalid Address
```bash
$ curl -X POST http://localhost:8000/validate-address \
  -H "Content-Type: application/json" \
  -d '{"address":"Random Street, Somewhere"}'

Response:
{
  "status": "invalid",
  "address": "Random Street, Somewhere",
  "message": "Address does not contain a recognized NZ suburb"
}
```

---

## Testing with Swagger UI

FastAPI automatically generates interactive documentation:

**URL**: `http://localhost:8000/docs`

You can test all endpoints directly from the browser:
1. Navigate to http://localhost:8000/docs
2. Click on each endpoint to expand
3. Click "Try it out"
4. Enter request parameters
5. Click "Execute"

---

## Frontend Integration

The frontend (`frontend/src/services/apiClient.js`) handles all API communication:

```javascript
// Login example
await apiClient.post('/login', { 
  username: 'user123', 
  password: 'password123' 
});

// Address validation example
await apiClient.post('/validate-address', { 
  address: 'Queen Street, Auckland' 
});

// Health check example
await apiClient.get('/health');
```

---

## Future Enhancements

### Real NZ Post API Integration
The `backend/app/services/nz_post_real.py` contains a template for integrating with the real NZ Post API. To implement:

1. Obtain NZ Post API credentials
2. Set `NZ_POST_API_KEY` in `.env`
3. Implement actual API calls in `nz_post_real.py`
4. Update `address.py` routes to use real service

### JWT Authentication
Replace mock authentication with proper JWT tokens:
- Issue token on `/login`
- Validate token on protected endpoints
- Add token expiration

---

## Rate Limiting
Not currently implemented. Consider adding for production:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

---

## Logging
All requests are logged. Check console output when running:
```
python -m uvicorn app.main:app --reload
```

---

## Version
- **API Version**: 1.0.0
- **Frontend**: React 18 + Vite
- **Backend**: FastAPI
- **Python**: 3.9+
- **Node.js**: 16+
