# Playwright Automation Testing - Docker Setup

This document explains the Docker setup for running Playwright automation tests for the NZ Address Checker application.

## Overview

The automation testing setup consists of:

1. **automation.Dockerfile** - Container for running Playwright tests
2. **docker-compose.yml** - Orchestrates all services (backend, frontend, automation)
3. **GitHub Actions Workflow** - CI/CD pipeline for automated test execution

## Architecture

### Services

- **address-checker-api** (Backend)
  - FastAPI application on port 8000
  - Handles address validation through NZ Post API
  
- **address-checker-frontend** (Frontend)
  - Vue.js + Vite application on port 8080
  - Cognito authentication integration
  
- **address-checker-automation** (Automation)
  - Playwright test runner
  - Runs smoke and sanity tests
  - Generates HTML test reports

### Network

All services communicate via a custom Docker network `app-network` for isolated, secure communication.

## Local Testing

### Prerequisites

- Docker & Docker Compose installed
- Environment variables set (see Configuration)

### Running Tests Locally

```bash
# Navigate to docker directory
cd docker

# Build and start all services (including tests)
docker-compose up

# Or build without starting automation tests
docker-compose up -d backend frontend

# Run tests separately
docker-compose run --rm automation
```

### Accessing Services

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- Test Reports: `docker/test-results/report.html` (after tests run)

## Configuration

### Environment Variables

Create a `.env` file in the `docker/` directory:

```bash
# Cognito Configuration
VITE_COGNITO_DOMAIN=https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=4p7i1nq2t426jufkh0pe7fgo2u
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
VITE_COGNITO_SCOPE=email+openid+phone

# Test Credentials
TEST_USER_EMAIL=test-user@example.com
TEST_USER_PASSWORD=TestPassword123!

# API Configuration
VITE_API_BASE_URL=http://address-checker-api:8000
```

### GitHub Actions Secrets

For CI/CD pipeline, configure these secrets in GitHub Settings > Secrets and variables > Actions:

- `COGNITO_DOMAIN` - AWS Cognito domain
- `COGNITO_CLIENT_ID` - Cognito application client ID
- `TEST_USER_EMAIL` - Test account email
- `TEST_USER_PASSWORD` - Test account password

## GitHub Actions Pipeline

### Workflow: automation-tests.yml

Runs on:
- Push to `main` and `practice` branches
- Pull requests to `main` and `practice` branches

Steps:
1. Build Docker images (backend, frontend, automation)
2. Start backend and frontend services
3. Wait for services to be healthy
4. Run Playwright tests (smoke + sanity)
5. Generate test reports and screenshots
6. Upload artifacts
7. Comment on PR with results

### Artifacts

- `playwright-report/` - HTML test report (retained 30 days)
- `test-screenshots/` - Failed test screenshots (retained 7 days)

## Test Execution

### Smoke Tests (3 tests)

- SMOKE-001: Valid login with Cognito
- SMOKE-002: Address suggestions loading
- SMOKE-003: Valid address validation

### Sanity Tests (5 tests)

- SANITY-001: Invalid login handling
- SANITY-002: User logout
- SANITY-003: Address suggestion selection
- SANITY-004: Invalid address validation
- SANITY-005: Complete address workflow

### Test Configuration

Tests run with:
- `HEADLESS=true` in CI/CD (no browser window)
- `HEADLESS=false` for local debugging
- `SLOW_MO=0` in CI (fast execution)
- `SLOW_MO=1000` for local observation
- `TIMEOUT=30000` (30 seconds per operation)

## Debugging Failed Tests

### View Test Reports

```bash
# After local test run
open docker/test-results/report.html

# Or from GitHub Actions
# Download "playwright-report" artifact
```

### Check Screenshots

Failed tests automatically capture screenshots:
- Local: `docker/screenshots/`
- CI/CD: Download "test-screenshots" artifact

### View Logs

```bash
# Show logs from specific service
docker-compose logs automation
docker-compose logs frontend
docker-compose logs backend
```

## Building Automation Image

```bash
# Build just the automation image
docker build -f docker/automation.Dockerfile -t address-checker-automation:latest .

# Build all images
cd docker && docker-compose build
```

## Health Checks

All services include health checks:

- **Backend**: HTTP GET to `/health` endpoint
- **Frontend**: HTTP GET to root path
- **Tests**: Wait for both services to be healthy before starting

Services are considered healthy after:
- First successful health check
- Up to 3 retry attempts
- 5-10 second intervals

## Troubleshooting

### Tests Cannot Connect to Frontend

```bash
# Check if frontend is accessible
docker exec address-checker-automation curl http://address-checker-frontend

# Check container logs
docker logs address-checker-frontend
```

### Tests Hang or Timeout

- Increase `TIMEOUT` environment variable
- Check Docker resource limits
- Verify Cognito credentials are correct
- Check network connectivity to Cognito endpoints

### Selectors Not Found

- Screenshots are saved to debug selector issues
- Update selectors in `tests/pages/login_page.py` and `tests/pages/main_page.py`
- Run tests with `HEADLESS=false` to observe browser behavior

## Best Practices

1. **Run locally before pushing** - Test changes locally first
2. **Check artifacts on failure** - Always review screenshots and reports
3. **Keep credentials secure** - Use GitHub Secrets, never commit credentials
4. **Update selectors carefully** - Test selector changes in isolation
5. **Review logs** - Check test output for warnings or errors

## Files Reference

- `docker/automation.Dockerfile` - Automation container definition
- `docker/docker-compose.yml` - Service orchestration
- `.github/workflows/automation-tests.yml` - GitHub Actions workflow
- `tests/conftest.py` - Pytest configuration and fixtures
- `tests/smoke/test_smoke.py` - Smoke test suite
- `tests/sanity/test_sanity.py` - Sanity test suite
- `tests/pages/` - Page Object Model classes
- `tests/utils/` - Helper functions and test data

## Future Enhancements

- [ ] Parallel test execution across multiple browsers
- [ ] Visual regression testing
- [ ] Performance benchmarking
- [ ] Custom reporting dashboard
- [ ] Integration with Slack/Teams notifications
- [ ] Test result archival and trending
