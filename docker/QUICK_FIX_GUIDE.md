# How to Fix Test Failures - Quick Start

## Root Cause

Tests were failing because **Cognito authentication was not configured** in the Docker environment. The app's login page was showing an error instead of redirecting to Cognito.

## What Was Fixed

1. ✓ Created `docker/.env` with Cognito credentials
2. ✓ Updated `docker/.env` to use Docker network hostnames (address-checker-api instead of localhost)
3. ✓ Updated docker-compose.yml with proper environment variables
4. ✓ Created debug documentation

## How to Test Now

### Step 1: Start Docker Services

```bash
cd docker
docker-compose down    # Clean up old containers
docker-compose build   # Rebuild with new env vars
docker-compose up      # Start all services
```

Wait 30-45 seconds for services to start and health checks to pass.

### Step 2: Verify Frontend Works

Open browser to: **http://localhost:8080**

You should see:
- Page title: "NZ Address Checker"
- A blue "Login" button (ENABLED, not disabled)
- No error message

### Step 3: Verify Backend API

```bash
curl http://localhost:8000/health
```

Should return: `{"status": "healthy"}`

### Step 4: Run Tests

In a new terminal:

```bash
cd docker
docker-compose run --rm automation
```

This will:
- Launch Playwright Chromium browser
- Navigate to frontend
- Click Login button
- Get redirected to AWS Cognito
- Enter test credentials
- Run 8 tests (3 smoke + 5 sanity)
- Generate HTML report in `test-results/report.html`
- Capture screenshots in `screenshots/` if tests fail

### Step 5: Check Results

After tests complete, check:
```bash
# View test report
open test-results/report.html

# Or view screenshots if tests failed
ls -la screenshots/
```

## What Changed

### File: `docker/.env` (Updated)

```bash
# Now includes:
VITE_API_BASE_URL=http://address-checker-api:8000      # Docker network
VITE_COGNITO_DOMAIN=https://ap-southeast-22oqqdaka4...   # AWS Cognito domain
VITE_COGNITO_CLIENT_ID=4p7i1nq2t426jufkh0pe7fgo2u       # Cognito client ID
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
VITE_COGNITO_SCOPE=email+openid+phone

# Test credentials
TEST_USER_EMAIL=test-user@example.com
TEST_USER_PASSWORD=TestPassword123!

# Automation settings
BASE_URL=http://address-checker-frontend
BACKEND_URL=http://address-checker-api:8000
```

### Why This Fixes It

1. **Cognito config now provided** - Frontend app can now detect Cognito is configured
2. **Login button enabled** - App redirects to Cognito instead of showing error
3. **Tests can login** - Playwright can click login button and proceed through auth flow
4. **Docker network** - Services communicate via Docker network (not localhost)

## Expected Test Flow

```
1. Test starts Chromium browser
2. Navigate to http://address-checker-frontend (inside Docker network)
3. App displays login page with enabled "Login" button
4. Test clicks Login button
5. Browser redirects to AWS Cognito hosted UI
6. Test enters credentials (test-user@example.com / TestPassword123!)
7. Cognito redirects back to app with JWT token
8. App stores token in localStorage
9. Test verifies authentication successful
10. Test proceeds through smoke/sanity test scenarios
11. Report generated
```

## Troubleshooting

### Tests still fail to login

**Problem**: Can't find Cognito login form elements

**Solution**: 
```bash
# Run debug script to see actual page structure
python tests/debug_cognito.py

# Check screenshot
open tests/debug_cognito_page.png

# Update selectors in tests/pages/login_page.py based on what you see
```

### Frontend shows error message

**Problem**: Cognito configuration not loaded

**Solution**:
```bash
# Verify env vars are in docker/.env
cat docker/.env

# Rebuild (env vars embedded during build)
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Tests timeout

**Problem**: Services not ready

**Solution**:
```bash
# Check logs
docker-compose logs frontend
docker-compose logs backend
docker-compose logs automation

# Increase timeout in docker/.env
TIMEOUT=60000  # 60 seconds instead of 30
```

### Can't access app at localhost:8080

**Problem**: Port not exposed or app not running

**Solution**:
```bash
# Check if containers are running
docker-compose ps

# Check port mapping
docker port address-checker-frontend

# If not running, start:
docker-compose up -d
```

## Files Created/Modified

- ✓ Created: `docker/TEST_FAILURE_DEBUG.md` - Detailed root cause analysis
- ✓ Created: `tests/debug_cognito.py` - Debug script to inspect Cognito page
- ✓ Modified: `docker/.env` - Added Cognito credentials and test config
- ✓ Modified: `tests/conftest.py` - Fixed import errors
- ✓ Modified: `tests/pages/base_page.py` - Fixed import errors
- ✓ Modified: `tests/pages/login_page.py` - Updated Cognito selectors

## Next Steps

1. Run `docker-compose up` to start services
2. Verify login button works in browser
3. Run `docker-compose run --rm automation` to execute tests
4. Review `test-results/report.html` for results
5. If tests still fail, run `debug_cognito.py` script
6. Update Cognito selectors as needed
7. Commit and push successful version

## Success Indicators

Tests passing:
- HTML report shows 8/8 PASSED
- No screenshots in `screenshots/` directory
- All smoke and sanity test scenarios work

Tests failing:
- HTML report shows failures
- Screenshots captured for failed tests
- Check `docker/screenshots/` for visual debugging
