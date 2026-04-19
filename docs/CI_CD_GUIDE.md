# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for continuous integration and deployment. The pipeline automatically runs tests, security scans, and builds on every push and pull request.

## Workflows

### 1. **Backend CI** (`.github/workflows/backend.yml`)
Runs on changes to `backend/**` directory.

**Jobs:**
- **lint-and-test**
  - Sets up Python 3.12
  - Installs dependencies
  - Runs pylint for code quality (threshold: 7.0)
  - Checks code formatting with Black
  - Validates import sorting with isort
  - Verifies backend imports successfully
  
- **security-scan**
  - Runs Bandit for security vulnerabilities
  - Generates and uploads security reports

**Triggers:**
- Push to `practice` branch
- Pull requests to `practice` branch

### 2. **Frontend CI** (`.github/workflows/frontend.yml`)
Runs on changes to `frontend/**` directory.

**Jobs:**
- **lint-and-build**
  - Sets up Node.js 20.x
  - Installs dependencies with npm ci
  - Builds the application with Vite
  - Uploads build artifacts
  - Reports build size
  
- **security-scan**
  - Runs npm audit for vulnerabilities
  - Lists dependencies

**Triggers:**
- Push to `practice` branch
- Pull requests to `practice` branch

### 3. **Docker Build** (`.github/workflows/docker.yml`)
Builds and tests Docker images.

**Jobs:**
- **build-and-push**
  - Builds backend Docker image
  - Builds frontend Docker image
  - Tests Docker images for basic functionality
  - Scans with Trivy for vulnerabilities
  - Uploads security scan results

**Triggers:**
- Push to `practice` branch
- Changes to `docker/**` directory
- Manual trigger via `workflow_dispatch`

### 4. **Integration Tests** (`.github/workflows/integration-test.yml`)
Tests integration between components.

**Jobs:**
- **integration-tests**
  - Tests backend health endpoint with TestClient
  - Verifies all imports work correctly
  - Builds frontend application
  - Verifies build output

**Triggers:**
- Push to `practice` branch
- Pull requests

### 5. **Dependency Updates** (`.github/workflows/dependencies.yml`)
Checks for vulnerable or outdated dependencies.

**Jobs:**
- **check-python-deps**
  - Uses Safety to check Python dependencies
  - Reports outdated packages
  
- **check-node-deps**
  - Runs npm audit
  - Reports outdated packages

**Triggers:**
- Changes to requirements or package files
- Weekly schedule (Sunday at 00:00 UTC)

### 6. **Continuous Integration** (`.github/workflows/ci.yml`)
Master workflow that orchestrates all checks.

**Orchestrates:**
- Backend checks
- Frontend checks
- Integration tests
- Summary report

**Concurrency:** Cancels previous runs on new push

### 7. **Deploy** (`.github/workflows/deploy.yml`)
Production deployment pipeline.

**Jobs:**
- **build**
  - Builds Docker images with metadata
  - Optionally pushes to Docker registry
  
- **deploy**
- Runs only on `practice` branch
- Targets the `production` GitHub Environment
  - Placeholder for production deployment

**Requires Secrets:**
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub token

## Setup Instructions

### 1. Enable GitHub Actions
1. Go to repository Settings → Actions → General
2. Ensure "Allow all actions and reusable workflows" is selected
3. Configure action permissions as needed

### 2. Configure Secrets for Deployment

To enable Docker push on deploy:

```bash
# Navigate to Settings → Secrets and variables → Actions
# Create new repository secrets:
DOCKER_USERNAME  # Your Docker Hub username
DOCKER_PASSWORD  # Your Docker Hub access token
```

### 3. Configure Branch Protection

To require CI passes before merge:

1. Go to Settings → Branches
2. Add branch protection rule for `practice`
3. Require status checks to pass:
   - Backend Lint & Type Check
   - Frontend Lint & Build
   - Integration Tests
  - Secret & Credential Scanning
  - SonarCloud Analysis
4. Require branches to be up to date before merging

### 4. Configure Environment Approvals

To add manual approval gates before deployment:

1. Go to Settings → Environments
2. Create or open environment `production`
3. Add Required reviewers
4. (Optional) Restrict deployment branches to `practice`

The deploy job in `.github/workflows/deploy.yml` already targets the `production` environment.

### 5. Authenticated Workflow Monitoring (Avoid API Rate Limits)

Use a token when monitoring runs from scripts:

```powershell
$env:GH_TOKEN = "<github_pat_or_app_token>"
./scripts/monitor-actions.ps1 -Owner "NZ-Adddress-Checker" -Repo "Address-Checker-App" -Branch "practice" -Watch
```

Without `GH_TOKEN`, GitHub API polling can hit unauthenticated rate limits.

## Workflow Status Badges

Add these to your README.md:

```markdown
![Backend CI](https://github.com/YOUR_USERNAME/Address-Checker-App/actions/workflows/backend.yml/badge.svg)
![Frontend CI](https://github.com/YOUR_USERNAME/Address-Checker-App/actions/workflows/frontend.yml/badge.svg)
![Integration Tests](https://github.com/YOUR_USERNAME/Address-Checker-App/actions/workflows/integration-test.yml/badge.svg)
```

## Local Testing

To test workflows locally before pushing:

### Install act
```bash
# macOS
brew install act

# Windows (Chocolatey)
choco install act-cli
```

### Run a specific workflow
```bash
act -j backend-checks
act -j frontend-checks
act -j integration-tests
```

### Run all workflows
```bash
act
```

## Troubleshooting

### Workflow fails with "Module not found"
- Check Python version matches (3.12)
- Verify all dependencies in `requirements.txt` are installed
- Run locally: `pip install -r backend/requirements.txt`

### Frontend build fails
- Check Node.js version (20.x)
- Run locally: `npm ci && npm run build` in frontend directory
- Check for missing environment variables

### Docker build fails
- Verify Dockerfiles exist in `docker/` directory
- Run locally: `docker build -f docker/Dockerfile .`
- Check for missing files in .gitignore

### Security scans report false positives
- Add suppression rules in `.bandit` or `.pylintrc` if needed
- Review and update dependencies to latest secure versions

## Best Practices

1. **Keep workflows simple** - Each workflow should have a single responsibility
2. **Use caching** - Workflows cache npm and pip dependencies to speed up builds
3. **Fail fast** - Early detection of issues saves time
4. **Use consistent Python/Node versions** - Match production environment
5. **Regular dependency updates** - Automated weekly checks via scheduled workflow
6. **Protected branches** - Require CI passes before merging to main

## Performance Tips

- **Parallel jobs** - Most jobs run in parallel for faster feedback
- **Caching** - GitHub Actions caches dependencies automatically
- **Conditional steps** - Security scans use `continue-on-error` for reporting

## Next Steps

1. Customize workflows for your specific needs
2. Set up branch protection rules
3. Configure Docker Hub secrets for automated pushes
4. Monitor Actions tab for build results
5. Adjust linting thresholds as needed

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyLint Rules](https://pylint.pycqa.org/)
- [Black Formatting](https://black.readthedocs.io/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
