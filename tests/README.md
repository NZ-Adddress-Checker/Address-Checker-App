# Tests Directory

This directory contains all tests for the Address Checker application.

## Structure

- `backend/` - Backend unit and integration tests
- `frontend/` - Frontend component tests
- `e2e/` - End-to-end tests

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## CI/CD

Tests are automatically run on:
- Pull requests to `main` and `practice` branches
- Pushes to `main` and `practice` branches

See `.github/workflows/` for the complete CI/CD configuration.
