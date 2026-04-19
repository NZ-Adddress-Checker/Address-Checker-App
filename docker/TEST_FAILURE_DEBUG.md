# Test Failure Root Cause Analysis

## Problem Summary

Tests are failing because **Cognito is not configured in the Docker container**.

The frontend shows a "Login" button that should redirect to Cognito's hosted login page, but Cognito configuration variables are empty, so the button doesn't work.

## Root Cause

The Docker environment is missing the Cognito configuration environment variables:

```
VITE_COGNITO_DOMAIN           (empty - needs AWS Cognito domain)
VITE_COGNITO_CLIENT_ID        (empty - needs Cognito client ID)
VITE_COGNITO_REDIRECT_URI     (set correctly to http://localhost:8080/callback)
```

## Evidence

When we ran the debug script, it found:
- App is on `http://localhost:8080/`
- Page shows "NZ Address Checker" title
- Button text is "Login"
- **BUT**: The button calls `isCognitoConfigured()` which returns `false` because the env vars are empty
- When Cognito is not configured, the app shows an error message instead of redirecting

## Solution

You need to provide the Cognito credentials to the Docker container. There are two approaches:

### Option 1: Create a `.env` file in `docker/` directory

Create `docker/.env`:

```bash
VITE_COGNITO_DOMAIN=https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=4p7i1nq2t426jufkh0pe7fgo2u
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
VITE_COGNITO_SCOPE=email+openid+phone
VITE_API_BASE_URL=http://address-checker-api:8000
TEST_USER_EMAIL=test-user@example.com
TEST_USER_PASSWORD=TestPassword123!
```

Then run:
```bash
cd docker
docker-compose up
```

Docker Compose will automatically load `.env` and pass values to containers.

### Option 2: Pass variables via command line

```bash
cd docker

# Build with env vars
docker-compose build \
  --build-arg VITE_COGNITO_DOMAIN=https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com \
  --build-arg VITE_COGNITO_CLIENT_ID=4p7i1nq2t426jufkh0pe7fgo2u \
  --build-arg VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback

# Run
docker-compose up
```

### Option 3: Export as shell variables (for GitHub Actions)

In `.env` or when running tests, these should already be set from GitHub Secrets.

## How to Get Cognito Credentials

From your frontend `.env`:
- **VITE_COGNITO_DOMAIN**: `https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com`
- **VITE_COGNITO_CLIENT_ID**: `4p7i1nq2t426jufkh0pe7fgo2u`
- **VITE_COGNITO_REDIRECT_URI**: `http://localhost:8080/callback`

These come from your AWS Cognito setup.

## Expected Flow After Fix

1. **Local**: Navigate to `http://localhost:8080/`
   - See "Login" button (enabled)
   - Click it
   - Redirected to AWS Cognito hosted login page
   - Enter test credentials
   - Redirected back to app with JWT token

2. **Tests**: 
   - Playwright navigates to app
   - Clicks "Login" button
   - Gets redirected to Cognito
   - Enters credentials
   - Returns to app
   - Tests can verify authentication

## Files to Create/Update

1. **Create**: `docker/.env`
   ```bash
   VITE_COGNITO_DOMAIN=https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com
   VITE_COGNITO_CLIENT_ID=4p7i1nq2t426jufkh0pe7fgo2u
   VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
   VITE_COGNITO_SCOPE=email+openid+phone
   VITE_API_BASE_URL=http://address-checker-api:8000
   TEST_USER_EMAIL=test-user@example.com
   TEST_USER_PASSWORD=TestPassword123!
   ```

2. **Update**: `docker/docker-compose.yml` - Modify frontend service build args:
   ```yaml
   frontend:
     build:
       args:
         VITE_API_BASE_URL: ${VITE_API_BASE_URL:-http://address-checker-api:8000}
         VITE_COGNITO_DOMAIN: ${VITE_COGNITO_DOMAIN}  # Required, no default
         VITE_COGNITO_CLIENT_ID: ${VITE_COGNITO_CLIENT_ID}  # Required
         VITE_COGNITO_REDIRECT_URI: ${VITE_COGNITO_REDIRECT_URI:-http://localhost:8080/callback}
         VITE_COGNITO_SCOPE: ${VITE_COGNITO_SCOPE:-email+openid+phone}
   ```

## Next Steps

1. Copy Cognito credentials from `frontend/.env` to `docker/.env`
2. Run: `cd docker && docker-compose up`
3. Navigate to `http://localhost:8080/`
4. Verify login button is now enabled
5. Click login and go through Cognito flow
6. Run tests again

## Why Tests Are Failing

1. ✗ Cognito config is empty
2. ✗ Login button shows error or is disabled
3. ✗ Playwright can't click the login button
4. ✗ Tests fail because no login happens
5. ✓ Fix: Add Cognito env vars to docker/.env

## Additional Notes

- **Environment variables in Docker**: Values from `docker/.env` are only used during image build time for Vite (Vue.js frontend build)
- **Build-time vs runtime**: Cognito config must be available when Docker builds the frontend image
- **Vite** embeds these values into the compiled JavaScript during build
- This is why we need them in `.env` file or passed to `docker-compose build`
