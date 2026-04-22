# CI/CD Integration Guide
**NZ Address Checker Test Automation**

**Version:** 1.0  
**Last Updated:** April 22, 2026  
**Status:** Production Ready

---

## Table of Contents
1. [Overview](#overview)
2. [Supported Platforms](#supported-platforms)
3. [GitHub Actions Setup](#github-actions-setup)
4. [GitLab CI Setup](#gitlab-ci-setup)
5. [Pipeline Architecture](#pipeline-architecture)
6. [Configuration & Secrets](#configuration--secrets)
7. [Pipeline Stages](#pipeline-stages)
8. [Triggering Pipelines](#triggering-pipelines)
9. [Monitoring & Reporting](#monitoring--reporting)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)

---

## Overview

This test automation framework is **fully CI/CD ready** with pre-configured pipelines for:

- ✅ **GitHub Actions** (`.github/workflows/test.yml`)
- ✅ **GitLab CI** (`.gitlab-ci.yml`)
- ✅ Automated testing on every push/PR
- ✅ Daily regression testing
- ✅ Security scanning
- ✅ Code quality checks
- ✅ Deployment readiness validation

### Key Features

| Feature | GitHub Actions | GitLab CI |
|---------|---------------|-----------|
| **Automated Testing** | ✅ | ✅ |
| **Security Scanning** | ✅ | ✅ |
| **Code Quality** | ✅ | ✅ |
| **Matrix Testing** | ✅ | ✅ |
| **Scheduled Runs** | ✅ | ✅ |
| **Manual Triggers** | ✅ | ✅ |
| **Artifact Storage** | ✅ | ✅ |
| **Test Reports** | ✅ | ✅ |
| **Docker Support** | ✅ | ✅ |

---

## Supported Platforms

### GitHub Actions

**Requirements:**
- GitHub repository
- GitHub Actions enabled
- Secrets configured (see Configuration section)

**Location:** `.github/workflows/test.yml`

**Features:**
- Parallel test execution (matrix strategy)
- Test result publishing
- Artifact retention (30 days)
- Scheduled daily runs
- Manual workflow dispatch

---

### GitLab CI

**Requirements:**
- GitLab repository
- GitLab Runner configured
- Docker executor enabled
- Secrets configured (see Configuration section)

**Location:** `.gitlab-ci.yml`

**Features:**
- Multi-stage pipeline
- Docker-in-Docker support
- Test result integration
- Pipeline schedules
- Manual job triggers

---

## GitHub Actions Setup

### Step 1: Repository Setup

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit with CI/CD"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/nz-address-checker-automation.git
   git push -u origin main
   ```

2. **Verify workflow file exists:**
   - Location: `.github/workflows/test.yml`
   - Should be committed to repository

---

### Step 2: Configure Secrets

Navigate to: **Repository Settings → Secrets and Variables → Actions**

Add the following secrets:

| Secret Name | Value | Required | Purpose |
|-------------|-------|----------|---------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key | Yes | AWS Cognito authentication |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key | Yes | AWS Cognito authentication |
| `ADDRESSABLE_API_KEY` | A_xWMNLslywtPO2DQ8jiMg | Optional | Addressable API (for contract tests) |
| `SLACK_WEBHOOK_URL` | Your Slack webhook | Optional | Notifications |

**To create AWS credentials:**

1. Go to AWS IAM Console
2. Create new user for CI/CD
3. Attach policy: `AmazonCognitoPowerUser` (minimal access)
4. Generate access key
5. Copy credentials to GitHub Secrets

---

### Step 3: Enable Workflows

1. Go to **Actions** tab in GitHub repository
2. Enable workflows if prompted
3. Workflows will run automatically on:
   - Every push to `main`, `develop`, or `feature/**` branches
   - Every pull request
   - Daily at 2 AM UTC (scheduled)
   - Manual trigger via "Run workflow" button

---

### Step 4: Verify Pipeline

1. Make a commit and push:
   ```bash
   git commit --allow-empty -m "Trigger CI/CD pipeline"
   git push
   ```

2. Go to **Actions** tab
3. Watch pipeline execute
4. Verify all jobs complete successfully

**Expected Jobs:**
- ✅ Code Quality Checks
- ✅ Security Scan
- ✅ Build Application
- ✅ Automated Tests (Functional/Security/Error Handling)
- ✅ Full Regression Suite
- ✅ Performance Baseline
- ✅ Deployment Ready

---

## GitLab CI Setup

### Step 1: Repository Setup

1. **Push code to GitLab:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit with CI/CD"
   git remote add origin https://gitlab.com/YOUR_USERNAME/nz-address-checker-automation.git
   git push -u origin main
   ```

2. **Verify pipeline file exists:**
   - Location: `.gitlab-ci.yml`
   - Should be committed to repository

---

### Step 2: Configure CI/CD Variables

Navigate to: **Settings → CI/CD → Variables**

Add the following variables:

| Variable Name | Value | Protected | Masked | Type |
|---------------|-------|-----------|--------|------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key | ✅ | ✅ | Variable |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key | ✅ | ✅ | Variable |
| `ADDRESSABLE_API_KEY` | API key | ❌ | ✅ | Variable |

---

### Step 3: Configure GitLab Runner

**Option 1: Use GitLab Shared Runners**
- Enable in **Settings → CI/CD → Runners**
- Shared runners provided by GitLab

**Option 2: Use Specific Runner (Recommended for production)**

Install GitLab Runner:
```bash
# Linux
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-runner

# Register runner
sudo gitlab-runner register
```

Runner configuration:
- **Executor:** Docker
- **Default image:** python:3.9
- **Privileged mode:** Yes (for Docker-in-Docker)

---

### Step 4: Set Up Pipeline Schedule

Navigate to: **CI/CD → Schedules → New Schedule**

**Recommended Schedule:**
- **Description:** Daily Regression Tests
- **Interval:** `0 2 * * *` (Daily at 2 AM UTC)
- **Target branch:** `main`
- **Activated:** ✅ Yes

---

### Step 5: Verify Pipeline

1. Make a commit and push:
   ```bash
   git commit --allow-empty -m "Trigger CI/CD pipeline"
   git push
   ```

2. Go to **CI/CD → Pipelines**
3. Watch pipeline execute
4. Verify all stages complete

**Expected Stages:**
- ✅ Lint
- ✅ Security
- ✅ Build
- ✅ Test
- ✅ Regression
- ✅ Deploy Check

---

## Pipeline Architecture

### GitHub Actions Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    Trigger Event                        │
│   (Push / PR / Schedule / Manual)                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────┐
│  Lint Check   │         │ Security Scan│
│   (flake8,    │         │ (safety,     │
│    black)     │         │  bandit)     │
└───────┬───────┘         └──────┬───────┘
        │                        │
        └────────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Build & Start  │
            │  Application    │
            │   (Docker)      │
            └────────┬────────┘
                     │
        ┌────────────┴────────────┬─────────────┐
        │                         │             │
        ▼                         ▼             ▼
┌──────────────┐         ┌──────────────┐ ┌──────────────┐
│  Functional  │         │   Security   │ │    Error     │
│    Tests     │         │    Tests     │ │  Handling    │
│  (Matrix)    │         │   (Matrix)   │ │   (Matrix)   │
└──────┬───────┘         └──────┬───────┘ └──────┬───────┘
       │                        │                │
       └────────────┬───────────┴────────────────┘
                    │
                    ▼
         ┌────────────────────┐
         │  Full Regression   │
         │   (All Tests)      │
         └─────────┬──────────┘
                   │
                   ▼
         ┌────────────────────┐
         │   Performance      │
         │    Baseline        │
         └─────────┬──────────┘
                   │
                   ▼
         ┌────────────────────┐
         │ Deployment Ready   │
         │      Check         │
         └────────────────────┘
```

---

### GitLab CI Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                Pipeline Trigger                         │
│   (Push / MR / Schedule / Manual)                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   ┌─────────┐              ┌──────────┐
   │  Lint   │              │ Security │
   │ (Stage) │              │ (Stage)  │
   └────┬────┘              └────┬─────┘
        │                        │
        └───────────┬────────────┘
                    │
                    ▼
            ┌──────────────┐
            │    Build     │
            │   (Stage)    │
            └──────┬───────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Functional│ │ Security │ │  Error   │
│  Tests   │ │  Tests   │ │ Handling │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┼────────────┘
                  │
                  ▼
          ┌──────────────┐
          │  Regression  │
          │   (Stage)    │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ Deploy Check │
          │   (Stage)    │
          └──────────────┘
```

---

## Configuration & Secrets

### Required Secrets

#### AWS Cognito Credentials

**Purpose:** Authenticate test users via AWS Cognito

**How to create:**

1. **AWS Console → IAM → Users → Create User**
   ```
   User name: cicd-test-user
   Access type: Programmatic access
   ```

2. **Attach Policy:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "cognito-idp:InitiateAuth",
           "cognito-idp:AdminInitiateAuth",
           "cognito-idp:GetUser"
         ],
         "Resource": "arn:aws:cognito-idp:ap-southeast-2:*:userpool/ap-southeast-2_2oQQDAKa4"
       }
     ]
   }
   ```

3. **Copy Credentials:**
   - Access Key ID → `AWS_ACCESS_KEY_ID`
   - Secret Access Key → `AWS_SECRET_ACCESS_KEY`

---

### Optional Secrets

#### Addressable API Key

**Purpose:** Run contract tests (consumes API quota)

**Value:** `A_xWMNLslywtPO2DQ8jiMg`

**Note:** Contract tests are skipped by default to preserve quota. Only run on schedule or manual trigger.

---

#### Slack Notifications (Optional)

**Purpose:** Send pipeline status to Slack

**Setup:**
1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Add webhook URL as `SLACK_WEBHOOK_URL` secret
3. Uncomment notification steps in workflow

---

## Pipeline Stages

### Stage 1: Code Quality (Lint)

**Duration:** ~30 seconds

**Jobs:**
- **flake8:** Python code linting
- **black:** Code formatting check

**Pass Criteria:**
- No critical errors (E9, F63, F7, F82)
- Code formatting compliant with black

**Failure Action:** Pipeline continues (non-blocking)

---

### Stage 2: Security Scan

**Duration:** ~45 seconds

**Jobs:**
- **safety:** Dependency vulnerability scanning
- **bandit:** Security linter for Python code

**Pass Criteria:**
- No high/critical vulnerabilities in dependencies
- No security issues in code

**Failure Action:** Pipeline continues (non-blocking)

**Artifacts:**
- `bandit-report.json` (30 days retention)

---

### Stage 3: Build Application

**Duration:** ~2 minutes

**Jobs:**
- Build Docker images (frontend + backend)
- Start containers
- Health check verification

**Pass Criteria:**
- Docker build successful
- Containers start without errors
- Health endpoints return HTTP 200

**Failure Action:** Pipeline stops (blocking)

**Artifacts (on failure):**
- `docker-logs.txt` (7 days retention)

---

### Stage 4: Automated Tests (Matrix)

**Duration:** ~3-5 minutes (parallel execution)

**Jobs:**

1. **Functional Tests**
   - File: `Tests/test_ui_flow.py`
   - Tests: 4
   - Critical: Yes

2. **Security Tests**
   - Files: `test_backend_api.py`, `test_jwt_security.py`, `test_address_api.py`
   - Tests: 10
   - Critical: Yes

3. **Error Handling Tests**
   - File: `Tests/test_error_handling.py`
   - Tests: 3
   - Critical: No (continues on failure)

**Pass Criteria:**
- All critical tests pass (100%)
- Non-critical tests ≥95%

**Failure Action:**
- Critical test failure → Pipeline stops
- Non-critical failure → Pipeline continues

**Artifacts:**
- Test reports (HTML) - 30 days
- Screenshots (on failure) - 7 days

---

### Stage 5: Full Regression

**Duration:** ~2 minutes

**Jobs:**
- Run all tests (excluding contract tests)
- Optional: Run contract tests (manual/scheduled)

**Pass Criteria:**
- 16/16 tests pass (100%)
- Execution time <120 seconds

**Failure Action:** Pipeline stops

**Artifacts:**
- `report.html` - 30 days
- `contract-report.html` (if run) - 30 days
- Screenshots - 7 days

---

### Stage 6: Performance Baseline

**Duration:** ~2 minutes

**Jobs:**
- Measure test execution time
- Record baseline metrics

**Pass Criteria:**
- Execution time within acceptable range (<120s)

**Failure Action:** Non-blocking (informational)

**Runs On:** Main branch pushes only

---

### Stage 7: Deployment Ready

**Duration:** ~5 seconds

**Jobs:**
- Verify all quality gates passed
- Generate deployment summary

**Pass Criteria:**
- All previous stages successful

**Failure Action:** N/A (summary only)

**Output:**
- Deployment readiness report
- GitHub/GitLab summary

---

## Triggering Pipelines

### Automatic Triggers

#### GitHub Actions

| Event | Branches | Description |
|-------|----------|-------------|
| **Push** | `main`, `develop`, `feature/**` | On every code push |
| **Pull Request** | `main`, `develop` | On PR creation/update |
| **Schedule** | `main` | Daily at 2 AM UTC |

#### GitLab CI

| Event | Branches | Description |
|-------|----------|-------------|
| **Push** | `main`, `develop` | On every code push |
| **Merge Request** | All | On MR creation/update |
| **Schedule** | `main` | Daily at 2 AM UTC (configure manually) |

---

### Manual Triggers

#### GitHub Actions

1. Go to **Actions** tab
2. Select **Test Automation CI/CD** workflow
3. Click **Run workflow**
4. Choose branch
5. Optional: Check "Run contract tests"
6. Click **Run workflow** button

#### GitLab CI

1. Go to **CI/CD → Pipelines**
2. Click **Run pipeline**
3. Choose branch
4. Click **Run pipeline**

**Manual Jobs:**
- Contract tests (must be triggered manually to preserve quota)

---

## Monitoring & Reporting

### GitHub Actions Dashboard

**Location:** Repository → Actions tab

**View:**
- All workflow runs
- Job status (success/failure)
- Execution time
- Artifacts

**Test Results:**
- Automatically published via `EnricoMi/publish-unit-test-result-action`
- Viewable in PR checks
- Summary in workflow run

---

### GitLab CI Dashboard

**Location:** Repository → CI/CD → Pipelines

**View:**
- Pipeline status
- Stage details
- Job logs
- Artifacts

**Test Results:**
- Beautiful HTML reports with Playwright test details
- Viewable in MR widget
- Downloadable reports with screenshots

---

### Artifacts & Reports

#### Available Artifacts

| Artifact | Retention | Size | Download Location |
|----------|-----------|------|-------------------|
| Test Reports (HTML) | 30 days | ~500KB | Actions/Pipelines → Artifacts |
| Screenshots (failures) | 7 days | Varies | Actions/Pipelines → Artifacts |
| Docker Logs (failures) | 7 days | ~100KB | Actions/Pipelines → Artifacts |
| Security Reports | 30 days | ~20KB | Actions/Pipelines → Artifacts |

---

### Test Report Example

**HTML Report Contents:**
- Test execution summary
- Pass/fail counts
- Individual test results
- Failure details with stack traces
- Execution timestamps
- Environment information

**Access:**
1. Go to workflow/pipeline run
2. Scroll to **Artifacts** section
3. Download `test-report-*.html`
4. Open in browser

---

## Troubleshooting

### Common Issues

#### Issue 1: Docker Build Fails

**Symptoms:**
- Build stage fails
- Error: "Cannot connect to Docker daemon"

**Solution (GitHub Actions):**
```yaml
# Already configured in workflow
- uses: docker/setup-buildx-action@v3
```

**Solution (GitLab CI):**
```yaml
# Ensure privileged mode enabled
# Runner config: /etc/gitlab-runner/config.toml
[[runners]]
  [runners.docker]
    privileged = true
```

---

#### Issue 2: AWS Cognito Authentication Fails

**Symptoms:**
- Functional tests fail
- Error: "Unable to authenticate"

**Solution:**
1. Verify AWS credentials in secrets
2. Check IAM policy permissions
3. Verify Cognito user pool region (ap-southeast-2)
4. Ensure test users exist in Cognito

**Verify credentials locally:**
```bash
aws cognito-idp admin-initiate-auth \
  --user-pool-id ap-southeast-2_2oQQDAKa4 \
  --client-id 4p7i1nq2t426jufkh0pe7fgo2u \
  --auth-flow ADMIN_NO_SRP_AUTH \
  --auth-parameters USERNAME=valid_user@example.com,PASSWORD=SecurePassword123! \
  --region ap-southeast-2
```

---

#### Issue 3: Playwright Browser Not Found

**Symptoms:**
- Tests fail with "Executable not found"

**Solution (GitHub Actions):**
```yaml
# Already included in workflow
- name: Install Playwright browsers
  run: python -m playwright install chromium --with-deps
```

**Solution (GitLab CI):**
```yaml
# Use official Playwright image
image: mcr.microsoft.com/playwright/python:v1.40.0-focal
```

---

#### Issue 4: Tests Timeout

**Symptoms:**
- Tests fail with timeout errors
- Health checks fail

**Solution:**
```yaml
# Increase wait time after container startup
- sleep 10  # Change to sleep 20 if needed
```

**Check service health:**
```bash
# In pipeline logs, verify:
curl -f http://localhost:8001/api/health
curl -f http://localhost:8085
```

---

#### Issue 5: Rate Limit Exceeded (Addressable API)

**Symptoms:**
- Contract tests fail
- Error: "429 Too Many Requests"

**Solution:**
- Contract tests are skipped by default
- Only run on schedule or manual trigger
- Use VPN to reset IP-based rate limit
- Request higher quota from Addressable

---

### Debug Mode

#### GitHub Actions

Enable debug logging:
1. Go to **Settings → Secrets → Actions**
2. Add secret: `ACTIONS_RUNNER_DEBUG` = `true`
3. Add secret: `ACTIONS_STEP_DEBUG` = `true`
4. Re-run workflow

#### GitLab CI

View detailed logs:
1. Go to **CI/CD → Pipelines**
2. Click on pipeline
3. Click on failed job
4. View full log output

---

## Best Practices

### 1. Branch Protection

**GitHub:**
- Settings → Branches → Add rule
- Require status checks to pass
- Require pull request reviews
- Include administrators

**Recommended checks:**
- ✅ Functional Tests
- ✅ Security Tests
- ✅ Full Regression Suite

---

### 2. Scheduled Runs

**Purpose:**
- Catch external dependency issues (Cognito, Addressable API)
- Detect environment drift
- Validate test stability

**Recommended Schedule:**
- **Daily:** 2 AM UTC (low traffic time)
- **Weekly:** Full regression with contract tests (Sundays)

---

### 3. Artifact Management

**Retention Policy:**
- Test reports: 30 days (regulatory compliance)
- Screenshots: 7 days (debugging only)
- Logs: 7 days (debugging only)
- Security reports: 30 days (audit trail)

**Storage Optimization:**
- Use `--self-contained-html` for HTML reports (single file)
- Compress large artifacts
- Clean up old artifacts periodically

---

### 4. Secret Rotation

**Schedule:**
- AWS credentials: Every 90 days
- API keys: When notified by provider
- Webhook URLs: When changing integrations

**Process:**
1. Generate new credentials
2. Update in CI/CD secrets
3. Test pipeline
4. Deactivate old credentials

---

### 5. Notifications

**Configure alerts for:**
- ❌ Pipeline failures (critical)
- ✅ Successful deployments (main branch)
- ⚠️ Scheduled run failures (daily regression)

**Platforms:**
- Slack (recommended)
- Microsoft Teams
- Email
- PagerDuty (for critical alerts)

---

### 6. Performance Monitoring

**Track:**
- Test execution time trends
- Docker build time
- Service startup time
- Pipeline duration

**Alert when:**
- Execution time increases >20%
- Pipeline duration >10 minutes
- Consistent failures

---

### 7. Test Stability

**Monitor:**
- Flaky test rate (<2% acceptable)
- Pass rate consistency (>98%)
- External dependency failures

**Action:**
- Fix flaky tests immediately
- Add retry logic for network-dependent tests
- Document known external issues

---

## Summary

### CI/CD Ready Checklist

✅ **Pipeline Configuration**
- ✅ GitHub Actions workflow configured
- ✅ GitLab CI pipeline configured
- ✅ Multi-stage pipeline with quality gates
- ✅ Parallel test execution (matrix strategy)

✅ **Security & Quality**
- ✅ Dependency vulnerability scanning (safety)
- ✅ Code security scanning (bandit)
- ✅ Code quality checks (flake8, black)

✅ **Testing**
- ✅ Functional tests automated
- ✅ Security tests automated
- ✅ Error handling tests automated
- ✅ Full regression suite
- ✅ Contract tests (manual/scheduled)

✅ **Reporting**
- ✅ HTML test reports (Playwright)
- ✅ Artifact storage (30 days)
- ✅ Screenshots on failure

✅ **Deployment**
- ✅ Deployment readiness checks
- ✅ Quality gate enforcement
- ✅ Automated validation

---

## Quick Start Commands

### Test Pipeline Locally (Docker)

```bash
# Start application
cd ../address-checker-app
docker compose up -d

# Run tests
cd ../nz-address-checker-automation
python -m pytest -v --tb=short --html=report.html --self-contained-html

# View report
open report.html  # macOS
start report.html  # Windows
```

---

### Validate Pipeline Files

**GitHub Actions:**
```bash
# Install actionlint
brew install actionlint  # macOS
# or download from https://github.com/rhysd/actionlint

# Validate workflow
actionlint .github/workflows/test.yml
```

**GitLab CI:**
```bash
# Use GitLab CI Lint
# Go to: CI/CD → Editor → Validate
# Or use API:
curl --header "PRIVATE-TOKEN: <your_token>" \
     "https://gitlab.com/api/v4/ci/lint" \
     --data "content=$(cat .gitlab-ci.yml)"
```

---

## Next Steps

1. ✅ **Configure Secrets** in your CI/CD platform
2. ✅ **Push Code** to trigger first pipeline run
3. ✅ **Verify** all stages pass
4. ✅ **Set Up Schedules** for daily regression
5. ✅ **Configure Notifications** for your team
6. ✅ **Enable Branch Protection** rules
7. ✅ **Monitor** pipeline runs and optimize

---

**For support, see:**
- [Test Plan](TEST_PLAN.md) - Complete test planning
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues
- [Architecture Guide](ARCHITECTURE.md) - Framework design

---

**End of CI/CD Integration Guide**
