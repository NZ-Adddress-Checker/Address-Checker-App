# Test Plan Document
**NZ Address Checker Application**

**Version:** 1.0  
**Last Updated:** April 22, 2026  
**Document Owner:** QA Team  
**Status:** Active

---

## Table of Contents
1. [Document Control](#document-control)
2. [Executive Summary](#executive-summary)
3. [Test Scope](#test-scope)
4. [Test Objectives](#test-objectives)
5. [Test Approach](#test-approach)
6. [Test Environment](#test-environment)
7. [Test Data Management](#test-data-management)
8. [Test Schedule](#test-schedule)
9. [Test Resources](#test-resources)
10. [Entry and Exit Criteria](#entry-and-exit-criteria)
11. [Test Execution Process](#test-execution-process)
12. [Test Deliverables](#test-deliverables)
13. [Risk Management](#risk-management)
14. [Defect Management](#defect-management)
15. [Test Metrics & Reporting](#test-metrics--reporting)
16. [Approval & Sign-off](#approval--sign-off)

---

## Document Control

### Document Information

| Attribute | Details |
|-----------|---------|
| Document Title | Test Plan - NZ Address Checker Application |
| Version | 1.0 |
| Created Date | April 22, 2026 |
| Last Updated | April 22, 2026 |
| Document Owner | QA Team |
| Classification | Internal |
| Status | Active - Production Ready |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | April 22, 2026 | QA Team | Initial test plan creation with comprehensive coverage |

### Document References

| Document | Location | Purpose |
|----------|----------|---------|
| [Test Cases](TEST_CASES.md) | Documents/TEST_CASES.md | Detailed test specifications (TC-001 to TC-019) |
| [Test Strategy](TEST_STRATEGY.md) | Documents/TEST_STRATEGY.md | Overall testing approach and methodology |
| [Impact Analysis](IMPACT_ANALYSIS.md) | Documents/IMPACT_ANALYSIS.md | Change impact and deployment risk assessment |
| [Architecture Guide](ARCHITECTURE.md) | Documents/ARCHITECTURE.md | Technical architecture and framework design |
| [Troubleshooting Guide](TROUBLESHOOTING.md) | Documents/TROUBLESHOOTING.md | Common issues and resolution procedures |

---

## Executive Summary

### Purpose

This Test Plan defines the comprehensive testing strategy for the **NZ Address Checker Application**, a web-based address validation system utilizing AWS Cognito authentication and the Addressable API for New Zealand address data.

### Application Overview

**Business Purpose:**
- Provide authenticated users with accurate NZ address search and validation
- Integrate with Addressable API for real-time address suggestions
- Ensure secure access through AWS Cognito authentication

**Technical Stack:**
- **Frontend:** React 18 (Port 8085)
- **Backend:** FastAPI (Port 8001)
- **Authentication:** AWS Cognito (ap-southeast-2_2oQQDAKa4)
- **Address Data:** Addressable API (api.addressable.dev)
- **Test Framework:** Playwright 1.47.0 + Pytest 8.4.2

### Testing Summary

| Metric | Value |
|--------|-------|
| Total Test Cases | 19 |
| Automated Test Cases | 19 (100%) |
| Manual Test Cases | 0 |
| Critical Test Cases | 7 (37%) |
| High Priority Test Cases | 9 (47%) |
| Medium Priority Test Cases | 3 (16%) |
| Test Coverage | 100% of documented scenarios |
| Current Pass Rate | 100% (16 passed, 3 skipped) |

### Key Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Test Framework Setup | ✅ Completed | Done |
| Test Case Development | ✅ Completed | Done |
| Test Environment Configuration | ✅ Completed | Done |
| Initial Test Execution | ✅ Completed | Done |
| Documentation Complete | ✅ Completed | Done |
| Production Ready | ✅ Completed | Done |

---

## Test Scope

### In-Scope

#### Functional Testing
✅ **User Authentication & Authorization**
- Valid user login with correct credentials
- Invalid user access blocking
- User logout functionality
- Session management and token handling

✅ **Address Search Functionality**
- Address autocomplete/suggestion via Addressable API
- Dropdown selection requirement validation
- Address validation after selection
- Search input validation and error handling

✅ **API Integration**
- Backend API endpoint authentication enforcement
- Request/response validation
- Error response handling (401, 422 status codes)
- External API contract compliance (Addressable)

#### Security Testing
✅ **Authentication Security**
- JWT token validation and integrity
- Bearer token format enforcement
- Invalid/tampered token rejection
- Empty token handling

✅ **API Security**
- Endpoint authentication enforcement (suggest/validate)
- Unauthorized access prevention (401 responses)
- Token tampering detection

#### Error Handling & Resilience
✅ **Network Error Scenarios**
- API timeout handling and user feedback
- Slow API response UI responsiveness
- Network error recovery mechanisms

✅ **External API Contract**
- Addressable API response validation
- Schema compliance verification
- Data structure integrity

#### Non-Functional Testing
✅ **Performance**
- API response time validation
- UI responsiveness during slow API calls
- Browser automation performance

✅ **Compatibility**
- Chromium browser compatibility (Playwright)
- Docker container deployment

---

### Out-of-Scope

❌ **Not Covered in Current Phase:**

**Load & Performance Testing:**
- High-volume concurrent user testing
- API rate limit stress testing
- Database performance under load
- Memory leak detection over extended periods

**Cross-Browser Testing:**
- Firefox browser compatibility
- Safari browser compatibility
- Edge browser compatibility
- Mobile browser testing (iOS Safari, Chrome Mobile)

**Accessibility Testing:**
- WCAG 2.1 compliance validation
- Screen reader compatibility
- Keyboard navigation testing
- Color contrast validation

**Localization/Internationalization:**
- Multi-language support
- Date/time format localization
- Currency and number format localization

**Database Testing:**
- Data integrity validation (no database in current architecture)
- Data migration testing
- Backup and recovery procedures

**Mobile Application Testing:**
- Native mobile app testing
- Responsive design on actual mobile devices
- Touch gesture validation

**Third-Party API Testing (Beyond Contract):**
- AWS Cognito internal functionality
- Addressable API backend testing
- Infrastructure-level cloud service testing

---

## Test Objectives

### Primary Objectives

#### 1. Validate Core Functionality (Priority: 🔴 Critical)

**Goal:** Ensure all core user workflows function correctly end-to-end

**Success Criteria:**
- ✅ Users can successfully login with valid credentials
- ✅ Users can search for NZ addresses and receive suggestions
- ✅ Users can validate selected addresses
- ✅ Invalid users are blocked from accessing the system
- ✅ Users can logout successfully

**Test Cases:** TC-001, TC-002, TC-003, TC-004

**Acceptance:** 100% pass rate required

---

#### 2. Ensure Security & Authorization (Priority: 🔴 Critical)

**Goal:** Verify all authentication and authorization mechanisms work correctly

**Success Criteria:**
- ✅ All API endpoints require valid authentication
- ✅ Invalid/tampered JWT tokens are rejected
- ✅ Bearer token format is enforced
- ✅ Unauthorized access returns proper 401 responses

**Test Cases:** TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012

**Acceptance:** 100% pass rate required (zero security vulnerabilities)

---

#### 3. Validate External Integrations (Priority: 🔴 High)

**Goal:** Confirm proper integration with external services (AWS Cognito, Addressable API)

**Success Criteria:**
- ✅ AWS Cognito authentication works correctly
- ✅ Addressable API returns expected data format
- ✅ API responses include required fields
- ✅ Schema validation passes for all external responses

**Test Cases:** TC-001, TC-003, TC-017, TC-018, TC-019

**Acceptance:** 95%+ pass rate (external dependencies may have occasional issues)

---

#### 4. Verify Error Handling & Resilience (Priority: 🟡 High)

**Goal:** Ensure application gracefully handles errors and network issues

**Success Criteria:**
- ✅ Timeout errors display appropriate messages to users
- ✅ UI remains responsive during slow API calls
- ✅ Application recovers from network errors automatically
- ✅ Error messages are user-friendly and informative

**Test Cases:** TC-014, TC-015, TC-016

**Acceptance:** 100% pass rate for error handling logic

---

#### 5. Maintain Test Automation Coverage (Priority: 🟡 Medium)

**Goal:** Achieve and maintain 100% automation coverage of documented scenarios

**Success Criteria:**
- ✅ All 19 test scenarios automated
- ✅ Tests run reliably and consistently
- ✅ Test execution time under 2 minutes (currently ~92 seconds)
- ✅ HTML reports generated automatically

**Acceptance:** 100% automation coverage maintained

---

### Secondary Objectives

#### 6. Regression Prevention

**Goal:** Prevent defects from reoccurring after fixes

**Approach:**
- Run full test suite before each deployment
- Maintain test suite as part of CI/CD pipeline
- Update tests when new features are added

**Success Metric:** Zero regression defects in production

---

#### 7. Documentation Excellence

**Goal:** Maintain comprehensive, up-to-date test documentation

**Deliverables:**
- ✅ Test Cases Document (TC-001 to TC-019)
- ✅ Test Strategy Document
- ✅ Impact Analysis Document
- ✅ Test Plan Document
- ✅ Troubleshooting Guide

**Success Metric:** All documents current and accessible

---

## Test Approach

### Testing Methodology

#### Automated Testing (Primary Approach)

**Framework:** Playwright + Pytest

**Rationale:**
- Fast, reliable, and repeatable
- Supports UI, API, and integration testing
- Excellent for regression testing
- Enables CI/CD integration

**Coverage:** 100% (all 19 test cases automated)

**Test Types:**

1. **End-to-End UI Tests (4 tests)**
   - Complete user workflows via browser automation
   - Validates frontend-backend-external API integration
   - Tests: TC-001, TC-002, TC-003, TC-004

2. **API Tests (6 tests)**
   - Direct backend API endpoint testing
   - Validates authentication, authorization, validation
   - Tests: TC-005, TC-006, TC-011, TC-012, TC-013

3. **Security Tests (4 tests)**
   - JWT token integrity validation
   - Token format and authentication enforcement
   - Tests: TC-007, TC-008, TC-009, TC-010

4. **Error Handling Tests (3 tests)**
   - Network timeout and error simulation
   - UI responsiveness under adverse conditions
   - Tests: TC-014, TC-015, TC-016

5. **Contract Tests (3 tests - Skipped by default)**
   - External API schema validation
   - Addressable API contract compliance
   - Tests: TC-017, TC-018, TC-019
   - Note: Skipped to preserve API quota (100 requests/day)

---

### Test Levels

#### Unit Testing
**Status:** Out of scope for QA (handled by developers)
**Responsibility:** Development Team

#### Integration Testing
**Status:** ✅ Covered
**Approach:** 
- Backend-to-Cognito integration (TC-001, TC-003)
- Backend-to-Addressable API integration (TC-001, TC-002, TC-017-019)
- Frontend-to-Backend API integration (TC-001, TC-002, TC-005, TC-006)

#### System Testing
**Status:** ✅ Covered
**Approach:**
- Full end-to-end user flows (TC-001)
- Complete system functionality validation
- All components working together

#### Acceptance Testing
**Status:** ✅ Covered
**Approach:**
- User workflow validation (TC-001, TC-002, TC-004)
- Business requirement verification
- User experience validation

---

### Test Design Techniques

#### 1. Positive Testing
**Purpose:** Verify system works with valid inputs
**Examples:**
- TC-001: Valid user login and address search
- TC-002: Proper dropdown selection

#### 2. Negative Testing
**Purpose:** Verify system handles invalid inputs correctly
**Examples:**
- TC-003: Invalid user blocked
- TC-007: Invalid token rejected
- TC-013: Missing field returns 422

#### 3. Boundary Testing
**Purpose:** Test edge cases and limits
**Examples:**
- Empty token (TC-010)
- Missing bearer prefix (TC-009)

#### 4. Error Handling Testing
**Purpose:** Verify graceful error handling
**Examples:**
- TC-014: Timeout handling
- TC-015: Slow response handling
- TC-016: Error recovery

#### 5. Contract Testing
**Purpose:** Validate external API compliance
**Examples:**
- TC-017: Response structure validation
- TC-018: Required field validation
- TC-019: Schema validation

---

### Test Automation Strategy

#### Framework Architecture

```
nz-address-checker-automation/
├── Tests/                          # Test files
│   ├── test_ui_flow.py            # E2E UI tests (4 tests)
│   ├── test_backend_api.py        # Backend API tests (3 tests)
│   ├── test_jwt_security.py       # JWT security tests (3 tests)
│   ├── test_address_api.py        # Address API tests (3 tests)
│   ├── test_addressable_contract.py  # Contract tests (3 skipped)
│   └── test_error_handling.py     # Error handling tests (3 tests)
├── pages/                          # Page Object Model
│   ├── login_page.py              # Login page abstraction
│   ├── dashboard_page.py          # Dashboard page abstraction
│   └── no_access_page.py          # No access page abstraction
├── utils/                          # Utilities
│   └── jwt_helper.py              # JWT token manipulation
├── config.py                       # Configuration
├── conftest.py                     # Pytest fixtures
└── requirements.txt               # Dependencies
```

#### Design Patterns

**Page Object Model (POM):**
- Abstracts UI elements and interactions
- Improves maintainability and readability
- Reduces code duplication

**Fixtures (Pytest):**
- Browser setup/teardown
- Test data preparation
- Environment configuration

**Data-Driven Testing:**
- User credentials from config
- API endpoints from environment
- Test data externalized

---

### Test Execution Strategy

#### Daily Regression Testing
```powershell
# Run all active tests (16 tests - excluding skipped contract tests)
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"
python -m pytest -v --tb=short
```
**Duration:** ~92 seconds  
**Schedule:** Daily before deployment  
**Pass Criteria:** 100% pass rate (16/16 tests)

---

#### Pre-Deployment Testing
```powershell
# Run all tests including contract validation
python -m pytest -v --tb=short --run-contract-tests
```
**Duration:** ~120 seconds (with contract tests)  
**Schedule:** Before major releases  
**Pass Criteria:** ≥95% pass rate (18/19 minimum)

---

#### Smoke Testing (Critical Tests Only)
```powershell
# Run only Priority 1 tests
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow \
                Tests/test_ui_flow.py::test_invalid_user_blocked \
                Tests/test_backend_api.py::test_suggest_requires_auth \
                Tests/test_backend_api.py::test_validate_requires_auth \
                Tests/test_jwt_security.py::test_tampered_jwt_rejected \
                -v --tb=short
```
**Duration:** ~30 seconds  
**Schedule:** After infrastructure changes  
**Pass Criteria:** 100% pass rate (5/5 tests)

---

#### Contract Testing (Quota Preservation)
```powershell
# Run external API contract tests (use sparingly)
python -m pytest Tests/test_addressable_contract.py -v --tb=short
```
**Duration:** ~15 seconds  
**Schedule:** Before external API integration changes only  
**Pass Criteria:** 100% pass rate (3/3 tests)  
**⚠️ Note:** Consumes API quota (100 requests/day limit)

---

## Test Environment

### Environment Configuration

#### Development Environment

| Component | Details |
|-----------|---------|
| **Operating System** | Windows (Primary), Linux (Docker) |
| **Browser** | Chromium 1134 (Playwright) |
| **Python** | 3.9.7 |
| **Frontend** | React 18, Port 8085 (Docker) |
| **Backend** | FastAPI, Port 8001 (Docker) |
| **Docker** | Docker Compose (latest) |
| **Test Framework** | Playwright 1.47.0, Pytest 8.4.2 |

#### Test Automation Environment

**Location:** `C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation`

**Dependencies:**
```
playwright==1.47.0
pytest==8.4.2
pytest-playwright==0.7.1
pytest-html==4.2.0
requests==2.32.3
pyjwt==2.10.1
jsonschema==4.23.0
python-dotenv==1.0.1
boto3==1.35.95
```

---

### External Dependencies

#### AWS Cognito (Authentication)

| Attribute | Value |
|-----------|-------|
| **Service** | AWS Cognito User Pool |
| **Region** | ap-southeast-2 (Sydney) |
| **User Pool ID** | ap-southeast-2_2oQQDAKa4 |
| **Client ID** | 4p7i1nq2t426jufkh0pe7fgo2u |
| **Test Users** | valid_user@example.com, invalid_user@example.com |
| **Availability** | 99.9% SLA |

**Impact on Testing:**
- Critical dependency - tests fail if Cognito unavailable
- Region-specific (ap-southeast-2 only)
- Test users must be pre-configured in pool

---

#### Addressable API (Address Data)

| Attribute | Value |
|-----------|-------|
| **Service** | Addressable Address Autocomplete |
| **Endpoint** | https://api.addressable.dev/v2/autocomplete |
| **API Key** | A_xWMNLslywtPO2DQ8jiMg |
| **Rate Limit** | 100 requests/day (IP-based) |
| **Country** | New Zealand (NZ) |
| **Availability** | 99% uptime |

**Impact on Testing:**
- Contract tests (TC-017 to TC-019) consume quota
- VPN required to bypass IP rate limiting
- Tests marked as skipped by default to preserve quota
- Run contract tests only before API integration changes

---

### Environment Setup Procedure

#### 1. Docker Container Setup

```powershell
# Navigate to application directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"

# Build and start containers
docker-compose up --build -d

# Wait for startup (5 seconds)
Start-Sleep -Seconds 5

# Verify services running
docker-compose ps
```

**Expected Output:**
```
Name                        Command               State           Ports
---------------------------------------------------------------------------------
address-checker-app_backend_1    ...  Up      0.0.0.0:8001->8001/tcp
address-checker-app_frontend_1   ...  Up      0.0.0.0:8085->8085/tcp
```

---

#### 2. Health Check Validation

```powershell
# Check backend health
curl http://localhost:8001/api/health

# Check frontend accessibility
curl http://localhost:8085
```

**Expected:**
- Backend: HTTP 200 response
- Frontend: HTTP 200 response (HTML content)

---

#### 3. Test Environment Setup

```powershell
# Navigate to test directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

---

#### 4. Environment Verification

```powershell
# Run smoke test
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow -v --tb=short
```

**Expected:** Test passes successfully

---

### Environment Variables

**Location:** `config.py` or `.env` file (if used)

```python
# Backend URL
BACKEND_URL = "http://localhost:8001"

# Frontend URL
FRONTEND_URL = "http://localhost:8085"

# AWS Cognito Configuration
COGNITO_REGION = "ap-southeast-2"
COGNITO_USER_POOL_ID = "ap-southeast-2_2oQQDAKa4"
COGNITO_CLIENT_ID = "4p7i1nq2t426jufkh0pe7fgo2u"

# Test Users
VALID_USER_EMAIL = "valid_user@example.com"
VALID_USER_PASSWORD = "SecurePassword123!"
INVALID_USER_EMAIL = "invalid_user@example.com"
INVALID_USER_PASSWORD = "InvalidPassword123!"

# Addressable API
ADDRESSABLE_API_KEY = "A_xWMNLslywtPO2DQ8jiMg"
```

---

## Test Data Management

### Test User Accounts

#### Valid User (Primary Test Account)

| Attribute | Value |
|-----------|-------|
| Email | valid_user@example.com |
| Password | SecurePassword123! |
| Status | Active |
| Purpose | Positive testing scenarios |
| Used In | TC-001, TC-002, TC-004, TC-005, TC-006 |

**Responsibilities:**
- Maintain active status in Cognito
- Do not delete or disable
- Password must meet Cognito complexity requirements

---

#### Invalid User (Negative Test Account)

| Attribute | Value |
|-----------|-------|
| Email | invalid_user@example.com |
| Password | InvalidPassword123! |
| Status | Not in Cognito pool |
| Purpose | Negative testing (access denial) |
| Used In | TC-003 |

**Responsibilities:**
- Ensure this user does NOT exist in Cognito
- Used to validate access blocking

---

### Test Address Data

#### NZ Address Examples

**Primary Test Address:**
```
Query: "10 Queen"
Expected Results: List of addresses containing "10 Queen Street" variants
Example: "10 Queen Street, Auckland Central, Auckland 1010"
```

**Used In:** TC-001, TC-002, TC-017, TC-018, TC-019

**Alternative Test Addresses:**
- "1 Victoria Street" (Wellington CBD)
- "123 Lambton Quay" (Wellington)
- "50 Customhouse Quay" (Auckland)

---

### API Test Data

#### Backend API Endpoints

| Endpoint | Method | Auth Required | Test Cases |
|----------|--------|---------------|------------|
| /api/address/suggest | POST | Yes | TC-001, TC-002, TC-005, TC-012 |
| /api/address/validate | POST | Yes | TC-001, TC-002, TC-006, TC-011, TC-013 |
| /api/health | GET | No | Manual health checks |

#### Request Payloads

**Suggest Request:**
```json
{
  "query": "10 Queen"
}
```

**Validate Request:**
```json
{
  "address_id": "12345",
  "formatted_address": "10 Queen Street, Auckland Central, Auckland 1010"
}
```

---

### JWT Token Test Data

**Valid Token:** Generated dynamically via AWS Cognito during test execution

**Invalid Tokens (for security testing):**
- Tampered token (TC-008): Modified signature
- No bearer prefix (TC-009): Missing "Bearer " prefix
- Empty token (TC-010): Empty string
- Invalid format (TC-007): Random string

---

### Data Management Strategy

#### Data Creation
- Test users: Pre-configured in AWS Cognito (manual setup)
- JWT tokens: Generated dynamically during test execution
- Address data: Sourced from live Addressable API

#### Data Cleanup
- No cleanup required (stateless application)
- JWT tokens expire automatically (1 hour TTL)
- No database to clean

#### Data Refresh
- Test users: Permanent (no refresh needed)
- API keys: Rotate when notified by provider
- Passwords: Update if Cognito policy changes

---

## Test Schedule

### Testing Timeline

#### Sprint/Release Cycle

**Cadence:** Continuous testing with deployment checkpoints

| Phase | Activities | Duration | Responsible |
|-------|-----------|----------|-------------|
| **Development** | Unit tests by developers | Ongoing | Dev Team |
| **Daily** | Automated regression (16 tests) | 2 minutes | CI/CD |
| **Pre-Deployment** | Full regression + smoke tests | 5 minutes | QA Team |
| **Pre-Release** | Full suite + contract tests | 10 minutes | QA Lead |
| **Post-Deployment** | Smoke tests + monitoring | 3 minutes | DevOps |
| **Post-Release** | Extended validation | 30 minutes | QA Team |

---

### Daily Testing Schedule

**Time:** Before each deployment (flexible timing)

**Activities:**
1. **Environment Check** (2 minutes)
   - Verify Docker containers running
   - Health check validation
   - Service availability confirmation

2. **Automated Test Execution** (2 minutes)
   - Run full test suite (excluding contract tests)
   - Generate HTML report
   - Review results

3. **Results Analysis** (1 minute)
   - Verify 100% pass rate
   - Check for flaky tests
   - Review execution time

**Total Time:** ~5 minutes

---

### Pre-Deployment Testing Schedule

**Trigger:** Before merging to main branch or deploying to production

**Activities:**

| Step | Activity | Duration | Pass Criteria |
|------|----------|----------|---------------|
| 1 | Code review completed | - | Approved by peer |
| 2 | Environment health check | 2 min | All services UP |
| 3 | Run smoke tests (Priority 1) | 30 sec | 100% pass (7/7) |
| 4 | Run full regression suite | 90 sec | 100% pass (16/16) |
| 5 | Review test report | 2 min | No failures, no errors |
| 6 | Approve deployment | - | QA sign-off |

**Total Time:** ~6 minutes  
**Go/No-Go Decision:** Based on 100% pass rate

---

### Release Testing Schedule

**Trigger:** Major releases, external API changes, infrastructure updates

**Activities:**

| Step | Activity | Duration | Pass Criteria |
|------|----------|----------|---------------|
| 1 | Environment setup (staging) | 5 min | Clean environment |
| 2 | Full regression suite | 90 sec | 100% pass (16/16) |
| 3 | Contract tests (if API changed) | 15 sec | 100% pass (3/3) |
| 4 | Security scan | 10 min | No critical vulnerabilities |
| 5 | Performance baseline | 5 min | Response times normal |
| 6 | User acceptance testing | 30 min | Business approval |
| 7 | Final approval | - | Release manager sign-off |

**Total Time:** ~50 minutes  
**Frequency:** Per major release (monthly or as needed)

---

### Ad-Hoc Testing Schedule

**Triggers:**
- Bug fixes
- Hotfixes
- Configuration changes
- Dependency updates

**Activities:**
- Run relevant subset of tests based on change type (see Impact Analysis)
- Minimum: Smoke tests (Priority 1)
- Recommended: Full regression for safety

---

## Test Resources

### Human Resources

#### QA Team Structure

| Role | Responsibility | Allocation |
|------|---------------|------------|
| **QA Lead** | Test planning, strategy, reporting | 25% |
| **Test Engineer** | Test execution, automation maintenance | 50% |
| **Test Engineer** | Test case development, documentation | 50% |
| **DevOps Engineer** | CI/CD integration, environment management | 25% |

**Total Team Effort:** ~150% FTE equivalent

---

#### Roles & Responsibilities

**QA Lead:**
- Test plan approval and maintenance
- Risk assessment and mitigation
- Test metrics reporting
- Stakeholder communication
- Release sign-off authority

**Test Engineers:**
- Test case execution and automation
- Defect identification and reporting
- Test environment maintenance
- Test data management
- Documentation updates

**DevOps Engineer:**
- CI/CD pipeline integration
- Docker container management
- Environment provisioning
- Deployment automation
- Infrastructure monitoring

---

### Technical Resources

#### Hardware Requirements

**Test Execution Machine:**
| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 50 GB free | 100 GB free |
| Network | Stable internet | High-speed (VPN for API) |

**Current Setup:**
- Windows workstation
- Sufficient resources for parallel test execution
- Docker Desktop installed and running

---

#### Software Requirements

**Required Software:**
| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.9.7+ | Test framework runtime |
| Docker | Latest | Application containers |
| Playwright | 1.47.0 | Browser automation |
| Pytest | 8.4.2 | Test runner |
| Git | Latest | Version control |
| VS Code | Latest (optional) | Test development |

**All Installed:** ✅ Yes

---

#### Test Tool Licenses

| Tool | License Type | Cost | Status |
|------|-------------|------|--------|
| Playwright | Apache 2.0 (Open Source) | Free | Active |
| Pytest | MIT (Open Source) | Free | Active |
| Python | PSF License (Open Source) | Free | Active |
| Docker Desktop | Free for small businesses | Free | Active |

**Total Licensing Cost:** $0

---

### Training Requirements

#### Team Training Needs

**New Team Members:**
- Playwright framework overview (4 hours)
- Page Object Model pattern (2 hours)
- Pytest fixtures and conventions (2 hours)
- Application architecture walkthrough (2 hours)
- **Total:** 10 hours onboarding

**Continuous Training:**
- Quarterly Playwright updates review (1 hour/quarter)
- Security testing best practices (annually)
- AWS Cognito changes (as needed)

---

## Entry and Exit Criteria

### Entry Criteria (Pre-Testing)

#### Before Starting Test Execution

**Environment Readiness:**
- ✅ Docker containers running (frontend + backend)
- ✅ Backend health check returns HTTP 200
- ✅ Frontend accessible at http://localhost:8085
- ✅ AWS Cognito service available
- ✅ Test users configured and active

**Code Readiness:**
- ✅ Code review completed and approved
- ✅ No critical compilation errors
- ✅ Developer unit tests passing
- ✅ Code merged to test branch

**Test Readiness:**
- ✅ Test cases reviewed and up-to-date
- ✅ Test data available
- ✅ Test environment configured
- ✅ Required access permissions granted

**Documentation:**
- ✅ Requirements documented
- ✅ Test cases traceable to requirements
- ✅ Known issues documented

---

### Exit Criteria (Testing Complete)

#### Daily Regression Testing

**Pass Criteria:**
- ✅ All 16 active tests passed (100% pass rate)
- ✅ No critical or high severity defects open
- ✅ Execution time under 120 seconds
- ✅ Test report generated successfully

**Failure Handling:**
- ❌ If ANY test fails → Do not proceed with deployment
- ❌ Investigate failure root cause
- ❌ Fix issue and re-run tests
- ❌ Obtain QA approval before deployment

---

#### Pre-Deployment Testing

**Pass Criteria:**
- ✅ All smoke tests (Priority 1) passed (7/7)
- ✅ All regression tests passed (16/16)
- ✅ No new defects introduced
- ✅ All critical defects resolved
- ✅ Test report reviewed by QA Lead
- ✅ Deployment approval documented

**Additional Checks:**
- ✅ Performance metrics within acceptable range
- ✅ No security vulnerabilities detected
- ✅ Rollback plan documented and tested
- ✅ Monitoring dashboards ready

---

#### Release Testing

**Pass Criteria:**
- ✅ Full test suite passed (16/16 active tests)
- ✅ Contract tests passed if API changes (3/3)
- ✅ User acceptance testing completed
- ✅ Security scan passed (no critical issues)
- ✅ Performance baseline validated
- ✅ All high and critical defects resolved
- ✅ All documentation updated
- ✅ Release notes prepared
- ✅ Stakeholder sign-off obtained

**Quality Gates:**
- ✅ Test coverage maintained at 100%
- ✅ Code coverage ≥80% (if tracked)
- ✅ No outstanding critical or high severity bugs
- ✅ All acceptance criteria met

---

### Suspension Criteria

**Testing Should Be Suspended If:**

❌ **Environment Issues:**
- Docker containers not running
- Backend or frontend services unavailable
- AWS Cognito service outage
- Addressable API unavailable (for contract tests)

❌ **Critical Defects:**
- Authentication completely broken
- Application crashes on startup
- Security vulnerability discovered
- Data corruption detected

❌ **Resource Constraints:**
- Test environment unavailable
- Required test data missing
- Key personnel unavailable (for critical testing)

**Resumption Criteria:**
- Root cause identified and resolved
- Entry criteria re-validated
- Impact assessment completed
- Management approval obtained

---

## Test Execution Process

### Test Execution Workflow

#### Standard Daily Execution

**Step-by-Step Process:**

**1. Pre-Execution Setup (2 minutes)**

```powershell
# Navigate to test directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"

# Verify Docker containers running
cd "../address-checker-app"
docker-compose ps

# If not running, start containers
docker-compose up -d

# Wait for services to be ready
Start-Sleep -Seconds 5

# Health check
curl http://localhost:8001/api/health
curl http://localhost:8085
```

**Expected:** Both services return HTTP 200

---

**2. Test Execution (2 minutes)**

```powershell
# Navigate back to test directory
cd "../nz-address-checker-automation"

# Run full test suite (excluding contract tests)
python -m pytest -v --tb=short --html=report.html --self-contained-html

# Wait for completion
```

**Expected Output:**
```
============================= test session starts =============================
platform win32 -- Python 3.9.7, pytest-8.4.2, pluggy-1.5.0
collected 19 items

Tests/test_ui_flow.py::test_valid_user_flow PASSED                      [  5%]
Tests/test_ui_flow.py::test_validation_requires_dropdown_selection PASSED [ 10%]
Tests/test_ui_flow.py::test_invalid_user_blocked PASSED                 [ 15%]
Tests/test_ui_flow.py::test_logout PASSED                               [ 20%]
Tests/test_backend_api.py::test_suggest_requires_auth PASSED            [ 25%]
Tests/test_backend_api.py::test_validate_requires_auth PASSED           [ 30%]
Tests/test_backend_api.py::test_invalid_token_rejected PASSED           [ 35%]
Tests/test_jwt_security.py::test_tampered_jwt_rejected PASSED           [ 40%]
Tests/test_jwt_security.py::test_no_bearer_prefix_rejected PASSED       [ 45%]
Tests/test_jwt_security.py::test_empty_token_rejected PASSED            [ 50%]
Tests/test_address_api.py::test_validate_without_auth_returns_401 PASSED [ 55%]
Tests/test_address_api.py::test_suggest_without_auth_returns_401 PASSED [ 60%]
Tests/test_address_api.py::test_validate_missing_field_returns_422 PASSED [ 65%]
Tests/test_error_handling.py::test_api_timeout_shows_error PASSED       [ 70%]
Tests/test_error_handling.py::test_slow_api_response_handling PASSED    [ 75%]
Tests/test_error_handling.py::test_network_error_recovery PASSED        [ 80%]
Tests/test_addressable_contract.py::test_addressable_returns_list SKIPPED [ 85%]
Tests/test_addressable_contract.py::test_addressable_items_have_formatted_field SKIPPED [ 90%]
Tests/test_addressable_contract.py::test_addressable_schema SKIPPED     [ 95%]

===================== 16 passed, 3 skipped in 92.52s ======================
```

---

**3. Results Analysis (1 minute)**

```powershell
# Open HTML report
Start-Process report.html

# Review results:
# - All 16 active tests passed ✅
# - 3 contract tests skipped (expected) ✅
# - Execution time reasonable (<120s) ✅
```

**Pass Criteria:**
- ✅ 16 passed
- ✅ 3 skipped (contract tests)
- ✅ 0 failed
- ✅ 0 errors

---

**4. Decision Making (<1 minute)**

**If All Tests Pass:**
- ✅ Proceed with deployment
- ✅ Update test log/tracker
- ✅ Archive test report

**If Any Tests Fail:**
- ❌ STOP - Do not deploy
- ❌ Review failure details in report
- ❌ Create defect ticket
- ❌ Notify development team
- ❌ Re-run after fix

---

### Test Execution Scenarios

#### Scenario 1: Smoke Testing (Post-Infrastructure Change)

**Purpose:** Quick validation after infrastructure changes

**Command:**
```powershell
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow \
                Tests/test_ui_flow.py::test_invalid_user_blocked \
                Tests/test_backend_api.py::test_suggest_requires_auth \
                Tests/test_backend_api.py::test_validate_requires_auth \
                Tests/test_jwt_security.py::test_tampered_jwt_rejected \
                -v --tb=short
```

**Duration:** ~30 seconds  
**Pass Criteria:** 5/5 tests passed

---

#### Scenario 2: Security Testing (Post-Auth Changes)

**Purpose:** Validate security after authentication changes

**Command:**
```powershell
python -m pytest Tests/test_backend_api.py \
                Tests/test_jwt_security.py \
                Tests/test_address_api.py \
                -v --tb=short
```

**Duration:** ~45 seconds  
**Pass Criteria:** 10/10 tests passed

---

#### Scenario 3: Contract Testing (Pre-API Integration Change)

**Purpose:** Validate external API contract before integration changes

**Command:**
```powershell
python -m pytest Tests/test_addressable_contract.py -v --tb=short
```

**Duration:** ~15 seconds  
**Pass Criteria:** 3/3 tests passed  
**⚠️ Warning:** Consumes API quota

---

#### Scenario 4: Functional Testing (Post-UI Changes)

**Purpose:** Validate UI changes don't break functionality

**Command:**
```powershell
python -m pytest Tests/test_ui_flow.py -v --tb=short
```

**Duration:** ~40 seconds  
**Pass Criteria:** 4/4 tests passed

---

### Defect Handling During Execution

#### Test Failure Workflow

**When a Test Fails:**

1. **Immediate Actions (0-5 minutes)**
   - ❌ STOP deployment process
   - 📸 Capture screenshot (if UI test)
   - 📝 Review error message and stack trace
   - 🔍 Check test report for details

2. **Initial Analysis (5-15 minutes)**
   - Determine if issue is test-related or application-related
   - Check if environment is healthy (services running)
   - Review recent code changes
   - Attempt to reproduce manually

3. **Classification (Immediate)**
   - **Test Issue (Flaky Test):** Fix test, re-run
   - **Application Defect:** Create defect ticket, notify team
   - **Environment Issue:** Fix environment, re-run
   - **Known Issue:** Verify if already documented

4. **Resolution Path**
   - **Critical Defect:** Stop deployment, fix immediately
   - **High Defect:** Assess risk, potentially block deployment
   - **Medium/Low Defect:** Document for future sprint

5. **Re-Testing**
   - Fix applied → Re-run failed test
   - Fix verified → Run full regression
   - All tests pass → Proceed with deployment

---

### Test Reporting During Execution

#### Real-Time Reporting

**Console Output:**
- Test name and status (PASSED/FAILED/SKIPPED)
- Progress percentage
- Execution time per test
- Final summary

**HTML Report:**
- Generated automatically after each run
- Location: `report.html` in test directory
- Self-contained (includes CSS/JS)
- Includes failure details, stack traces, screenshots

---

## Test Deliverables

### Primary Deliverables

#### 1. Test Cases Document ✅
**Status:** Complete  
**Location:** [Documents/TEST_CASES.md](TEST_CASES.md)  
**Content:**
- 19 detailed test cases (TC-001 to TC-019)
- Test case ID, category, priority
- Prerequisites, execution steps, expected results
- Actual automation code for each test
- Traceability matrix

**Update Frequency:** As tests are added/modified  
**Owner:** QA Team

---

#### 2. Test Execution Reports ✅
**Status:** Generated per execution  
**Location:** `report.html` (test directory)  
**Content:**
- Test execution summary (passed/failed/skipped)
- Execution time per test
- Failure details with stack traces
- Screenshots for failed UI tests (if applicable)
- Environment information

**Generation:** Automatic after each test run  
**Retention:** Last 10 reports archived

---

#### 3. Test Strategy Document ✅
**Status:** Complete  
**Location:** [Documents/TEST_STRATEGY.md](TEST_STRATEGY.md)  
**Content:**
- Testing approach and methodology
- Test types and coverage
- Tool selection rationale
- Success criteria

**Update Frequency:** Per release or major strategy change  
**Owner:** QA Lead

---

#### 4. Test Plan Document ✅
**Status:** Complete (this document)  
**Location:** [Documents/TEST_PLAN.md](TEST_PLAN.md)  
**Content:**
- Comprehensive test planning
- Scope, objectives, approach
- Schedule, resources, risks
- Entry/exit criteria

**Update Frequency:** Quarterly or as needed  
**Owner:** QA Lead

---

#### 5. Impact Analysis Document ✅
**Status:** Complete  
**Location:** [Documents/IMPACT_ANALYSIS.md](IMPACT_ANALYSIS.md)  
**Content:**
- Change impact assessment
- Component dependency mapping
- Deployment risk analysis
- Rollback procedures

**Update Frequency:** After architecture changes  
**Owner:** QA Team + DevOps

---

### Secondary Deliverables

#### 6. Defect Reports
**Status:** As needed  
**Location:** Issue tracking system (e.g., Jira, GitHub Issues)  
**Content:**
- Defect ID and title
- Severity and priority
- Steps to reproduce
- Expected vs actual results
- Environment details
- Screenshots/logs

**Template:**
```markdown
**Defect ID:** BUG-001
**Title:** Login fails with valid credentials
**Severity:** Critical
**Priority:** High
**Environment:** Docker, Windows, Chromium

**Steps to Reproduce:**
1. Navigate to http://localhost:8085
2. Enter valid_user@example.com
3. Enter SecurePassword123!
4. Click Login

**Expected:** User logged in successfully
**Actual:** Error message "Invalid credentials"

**Test Case:** TC-001
**Screenshots:** Attached
**Logs:** Backend logs attached
```

---

#### 7. Test Metrics Dashboard
**Status:** Available on request  
**Format:** Spreadsheet or dashboard  
**Content:**
- Test execution trends
- Pass/fail rates over time
- Defect density
- Test coverage percentage
- Execution time trends

**Update Frequency:** Weekly or per release  
**Owner:** QA Lead

---

#### 8. Test Environment Status Report
**Status:** Daily (if issues)  
**Content:**
- Service availability (Docker containers)
- External dependency status (Cognito, Addressable API)
- Environment configuration changes
- Known environment issues

---

### Deliverable Acceptance Criteria

**All Deliverables Must:**
- ✅ Be reviewed and approved by QA Lead
- ✅ Follow document templates and standards
- ✅ Include revision history
- ✅ Be stored in version control (Git)
- ✅ Be accessible to all stakeholders

---

## Risk Management

### Risk Assessment

#### High-Impact Risks

#### Risk 1: External Service Unavailability

**Risk Description:** AWS Cognito or Addressable API becomes unavailable

**Impact:** 🔴 Critical
- All tests dependent on these services will fail
- Unable to validate authentication or address functionality
- Deployment may be blocked

**Probability:** 🟡 Medium (5% chance)

**Mitigation Strategies:**
1. **Preventive:**
   - Monitor external service status pages
   - Set up service health check alerts
   - Maintain service SLA documentation

2. **Detective:**
   - Pre-test execution environment checks
   - Real-time monitoring during test execution

3. **Corrective:**
   - Re-run tests when service recovers
   - Document known outage periods
   - Communicate delays to stakeholders

**Contingency Plan:**
- If Cognito unavailable → Skip auth tests, document, proceed with caution
- If Addressable unavailable → Skip contract tests, validate manually if critical
- If both unavailable → Postpone testing, reschedule deployment

**Owner:** QA Lead + DevOps

---

#### Risk 2: Docker Container Failures

**Risk Description:** Docker containers crash or fail to start

**Impact:** 🔴 Critical
- All tests will fail
- Unable to execute any testing
- Deployment completely blocked

**Probability:** 🟡 Medium (10% chance)

**Mitigation Strategies:**
1. **Preventive:**
   - Regular Docker health checks
   - Maintain stable Docker images
   - Document container startup procedures

2. **Detective:**
   - Pre-execution health checks
   - Monitor container logs

3. **Corrective:**
   - Restart containers: `docker-compose restart`
   - Rebuild if needed: `docker-compose up --build -d`
   - Check logs: `docker-compose logs`

**Contingency Plan:**
```powershell
# Standard recovery procedure
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose down
docker-compose up --build -d
Start-Sleep -Seconds 10
curl http://localhost:8001/api/health
curl http://localhost:8085
```

**Owner:** DevOps Engineer

---

#### Risk 3: Test Data Corruption

**Risk Description:** Test user accounts deleted or passwords changed in Cognito

**Impact:** 🟡 High
- Authentication tests will fail
- Unable to validate login flows
- Deployment blocked until data restored

**Probability:** 🟢 Low (2% chance)

**Mitigation Strategies:**
1. **Preventive:**
   - Restrict access to Cognito user pool
   - Document test user accounts clearly
   - Implement least-privilege access

2. **Detective:**
   - Validate test user existence before test execution
   - Monitor Cognito audit logs

3. **Corrective:**
   - Recreate test users following documented procedure
   - Update passwords in config if changed
   - Re-run tests after restoration

**Contingency Plan:**
- Maintain backup Cognito pool configuration
- Document test user creation procedure
- Keep encrypted backup of test credentials

**Owner:** QA Team

---

#### Risk 4: API Rate Limit Exceeded

**Risk Description:** Addressable API rate limit (100 requests/day) exceeded

**Impact:** 🟡 Medium
- Contract tests fail
- Unable to validate external API integration
- May block API-related deployments

**Probability:** 🟡 Medium (15% chance if contract tests run frequently)

**Mitigation Strategies:**
1. **Preventive:**
   - Skip contract tests by default (currently implemented ✅)
   - Run contract tests only when necessary
   - Use VPN to reset IP-based limit
   - Request higher quota from Addressable

2. **Detective:**
   - Monitor API usage
   - Track test execution frequency

3. **Corrective:**
   - Wait for quota reset (24 hours)
   - Use VPN to change IP (temporary)
   - Manually validate API contract

**Contingency Plan:**
- Document when contract tests were last run
- Maintain manual API validation checklist
- Schedule contract tests strategically (e.g., once per week)

**Owner:** QA Team

---

### Medium-Impact Risks

#### Risk 5: Test Framework Updates Breaking Tests

**Impact:** 🟡 Medium  
**Probability:** 🟢 Low (5% chance)

**Mitigation:**
- Pin dependency versions in requirements.txt (currently implemented ✅)
- Test dependency updates in isolated environment
- Maintain changelog of framework updates

---

#### Risk 6: Network Connectivity Issues

**Impact:** 🟡 Medium  
**Probability:** 🟡 Medium (10% chance)

**Mitigation:**
- Run tests on stable network
- Implement retry logic for flaky network tests
- Document network requirements

---

#### Risk 7: Browser Compatibility Changes

**Impact:** 🟢 Low  
**Probability:** 🟢 Low (5% chance)

**Mitigation:**
- Playwright handles browser version management
- Pin Playwright version for stability
- Test on multiple browser versions if critical

---

### Risk Monitoring

**Risk Review Frequency:** Monthly or after major incidents

**Risk Metrics to Track:**
- External service uptime percentage
- Container failure frequency
- Test execution failure rate
- API quota utilization

**Risk Owner:** QA Lead

---

## Defect Management

### Defect Lifecycle

```
┌─────────────┐
│     NEW     │  ← Defect discovered during testing
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ASSIGNED   │  ← Assigned to developer
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ IN PROGRESS │  ← Developer working on fix
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   RESOLVED  │  ← Fix completed, ready for testing
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   VERIFIED  │  ← QA verified fix
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   CLOSED    │  ← Defect closed
└─────────────┘

Alternative path:
RESOLVED → REOPENED → ASSIGNED (if fix doesn't work)
```

---

### Defect Severity Classification

#### Critical (P1)

**Definition:** System unusable, critical functionality completely broken

**Examples:**
- Authentication completely fails for all users
- Application crashes on startup
- Security vulnerability allowing unauthorized access
- Data corruption or loss

**Response Time:** Immediate (within 1 hour)  
**Resolution Target:** Same day  
**Testing Impact:** Blocks all testing and deployment

**Handling:**
- Escalate immediately to development lead
- Stop all deployment activities
- Assign highest priority resources
- Continuous monitoring until resolved

---

#### High (P2)

**Definition:** Major functionality broken, workaround may exist

**Examples:**
- Address search returns incorrect results
- Logout doesn't invalidate session properly
- Error handling missing for critical flows
- API endpoint returns 500 errors intermittently

**Response Time:** Within 4 hours  
**Resolution Target:** Within 2 days  
**Testing Impact:** May block specific test areas

**Handling:**
- Assign to developer within 4 hours
- Daily status updates required
- QA validation required before closure

---

#### Medium (P3)

**Definition:** Non-critical functionality affected, workaround exists

**Examples:**
- UI display issues (styling problems)
- Error messages not user-friendly
- Minor validation issues
- Performance degradation (but within limits)

**Response Time:** Within 1 business day  
**Resolution Target:** Within 1 week  
**Testing Impact:** Does not block testing

**Handling:**
- Schedule for upcoming sprint
- Regular status updates
- Can be deferred if higher priority work exists

---

#### Low (P4)

**Definition:** Minor issues, cosmetic problems

**Examples:**
- Typos in UI text
- Minor alignment issues
- Suggestions for improvement
- Documentation errors

**Response Time:** Within 1 week  
**Resolution Target:** As time permits  
**Testing Impact:** No impact

**Handling:**
- Backlog for future sprints
- May be combined with other work
- Low priority for resolution

---

### Defect Reporting Template

```markdown
# Defect Report

## Basic Information
- **Defect ID:** [Auto-generated or BUG-XXX]
- **Title:** [Short, descriptive title]
- **Reported By:** [QA Team Member Name]
- **Reported Date:** [YYYY-MM-DD]
- **Severity:** [Critical/High/Medium/Low]
- **Priority:** [P1/P2/P3/P4]
- **Status:** [New/Assigned/In Progress/Resolved/Verified/Closed]
- **Assigned To:** [Developer Name]

## Test Information
- **Test Case ID:** [TC-XXX from TEST_CASES.md]
- **Test Execution ID:** [Report reference]
- **Environment:** [Docker/Windows/Chromium version]

## Defect Details

### Description
[Clear description of the defect]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

### Expected Result
[What should happen]

### Actual Result
[What actually happened]

### Frequency
[Always/Intermittent/Random]

### Workaround
[If any workaround exists]

## Supporting Information

### Screenshots
[Attach screenshots]

### Logs
```
[Paste relevant logs]
```

### Additional Context
[Any other relevant information]

## Root Cause Analysis (Filled by Developer)
[Root cause of the defect]

## Fix Description (Filled by Developer)
[Description of the fix]

## Verification Steps (For QA)
1. [Step 1 to verify fix]
2. [Step 2 to verify fix]
...

## Related Defects
[Link to related defects if any]
```

---

### Defect Metrics

**Track Monthly:**
- Total defects reported
- Defects by severity
- Defects by component (Frontend/Backend/Integration)
- Average time to resolution by severity
- Defect leakage to production (goal: 0)
- Reopened defects (goal: <5%)

**Quality Targets:**
- Critical defects in production: 0
- High defects in production: <2 per month
- Average resolution time P1: <24 hours
- Average resolution time P2: <48 hours

---

## Test Metrics & Reporting

### Key Performance Indicators (KPIs)

#### 1. Test Coverage

**Metric:** Percentage of documented scenarios with automated tests

**Current Status:** 100% (19/19 scenarios automated)

**Target:** Maintain 100%

**Measurement:**
```
Test Coverage = (Automated Test Cases / Total Test Scenarios) × 100
              = (19 / 19) × 100
              = 100%
```

**Tracking:** Monthly review of new scenarios vs automated tests

---

#### 2. Test Pass Rate

**Metric:** Percentage of tests passing in each execution

**Current Status:** 100% (16/16 active tests passing, 3 skipped)

**Target:** ≥98% for daily regression

**Measurement:**
```
Pass Rate = (Passed Tests / (Total Tests - Skipped Tests)) × 100
          = (16 / 16) × 100
          = 100%
```

**Tracking:** Daily automated test execution results

---

#### 3. Test Execution Time

**Metric:** Total time to execute full test suite

**Current Status:** ~92 seconds

**Target:** <120 seconds (2 minutes)

**Measurement:** Recorded automatically in test reports

**Tracking:** Monitor trends weekly, investigate if exceeds 120s

---

#### 4. Defect Detection Rate

**Metric:** Number of defects found per test execution cycle

**Current Status:** 0 (production-ready state)

**Target:** Varies by phase (higher during development, lower in production)

**Measurement:**
```
Defect Detection Rate = Defects Found / Test Executions
```

**Tracking:** Weekly summary during active development

---

#### 5. Defect Leakage Rate

**Metric:** Defects found in production that should have been caught in testing

**Current Status:** 0

**Target:** 0 critical/high defects, <2 medium/low per month

**Measurement:**
```
Leakage Rate = (Production Defects / Total Defects Found) × 100
```

**Tracking:** Monthly review of production incidents

---

#### 6. Test Automation ROI

**Metric:** Time saved by automation vs manual execution

**Calculation:**
```
Manual Execution Time per Test: ~5 minutes
Automated Execution Time per Test: ~5 seconds

Manual Suite Execution: 19 tests × 5 min = 95 minutes
Automated Suite Execution: 92 seconds ≈ 1.5 minutes

Time Saved per Execution: 95 - 1.5 = 93.5 minutes
Daily Executions: 1
Weekly Time Saved: 93.5 × 5 = 467.5 minutes ≈ 7.8 hours
```

**ROI:** Significant - automation pays for itself within first week

---

### Test Reporting

#### Daily Test Report (Automated)

**Format:** HTML Report (report.html)

**Content:**
- Test execution summary
  - Total tests: 19
  - Passed: 16
  - Failed: 0
  - Skipped: 3
  - Execution time: ~92 seconds
- Individual test results (PASSED/FAILED/SKIPPED)
- Failure details (if any)
- Environment information

**Distribution:** Automatic file generation, manual share if failures

**Frequency:** After each test execution

---

#### Weekly Test Summary

**Format:** Email or Dashboard

**Content:**
```
📊 Weekly Test Summary - Week of [Date]

✅ Test Executions: [X]
✅ Pass Rate: [Y%]
✅ Avg Execution Time: [Z seconds]

📈 Trends:
- Pass rate: [Up/Down/Stable]
- Execution time: [Up/Down/Stable]

🐛 Defects:
- New: [X]
- Resolved: [Y]
- Open: [Z]

🎯 Test Coverage: 100%

⚠️ Issues/Risks: [List any concerns]

📅 Next Week Plan: [Planned activities]
```

**Distribution:** QA Team, Dev Team, Management

**Frequency:** Every Monday

---

#### Monthly Test Metrics Report

**Format:** Detailed document or presentation

**Content:**
- KPI summary and trends
- Test coverage analysis
- Defect metrics (severity, resolution time, leakage)
- Test execution statistics
- Environment stability
- Risk assessment updates
- Recommendations and action items

**Distribution:** Stakeholders, Management

**Frequency:** First week of each month

---

#### Release Test Report

**Format:** Comprehensive document

**Content:**
- Executive summary
- Test scope and objectives
- Test execution results
  - Total test cases executed
  - Pass/fail breakdown by category
  - Critical test results
  - Contract test results (if run)
- Defect summary
  - Total defects found
  - Severity distribution
  - Resolved vs open defects
- Risk assessment
- Quality metrics
- Release recommendation (Go/No-Go)
- Sign-off section

**Distribution:** All stakeholders

**Frequency:** Per major release

---

### Metrics Dashboard (Recommended)

**Suggested Metrics for Dashboard:**

1. **Test Execution Trend (Last 30 Days)**
   - Line chart showing pass/fail/skip counts over time

2. **Pass Rate Trend**
   - Line chart showing daily pass rate percentage

3. **Execution Time Trend**
   - Line chart showing execution time over time

4. **Defect Status**
   - Pie chart showing open vs resolved defects

5. **Defect Severity Distribution**
   - Bar chart showing defects by severity

6. **Test Coverage**
   - Gauge showing current coverage percentage

**Tools:** Excel, Google Sheets, Tableau, or custom dashboard

---

## Approval & Sign-off

### Document Approval

**This Test Plan is approved by:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **QA Lead** | [Name] | _____________ | [Date] |
| **Development Lead** | [Name] | _____________ | [Date] |
| **DevOps Lead** | [Name] | _____________ | [Date] |
| **Product Owner** | [Name] | _____________ | [Date] |
| **Project Manager** | [Name] | _____________ | [Date] |

---

### Release Sign-off Template

**Use this template for each production release:**

```markdown
# Release Sign-off - Version [X.Y.Z]

## Release Information
- **Release Version:** [X.Y.Z]
- **Release Date:** [YYYY-MM-DD]
- **Release Type:** [Major/Minor/Patch/Hotfix]

## Test Execution Summary
- **Total Test Cases Executed:** [X]
- **Passed:** [X]
- **Failed:** [X]
- **Skipped:** [X]
- **Pass Rate:** [X%]
- **Test Report:** [Link to report.html]

## Critical Test Results
- ✅ TC-001 (Valid User Flow): PASSED
- ✅ TC-003 (Invalid User Blocked): PASSED
- ✅ TC-005 (API Auth - Suggest): PASSED
- ✅ TC-006 (API Auth - Validate): PASSED
- ✅ TC-007 (Invalid Token Rejected): PASSED
- ✅ TC-008 (Tampered JWT Rejected): PASSED
- ✅ TC-017 (Addressable Returns List): PASSED (if run)

## Defect Summary
- **Critical Defects:** [X] (must be 0)
- **High Defects:** [X] (all resolved/accepted)
- **Medium/Low Defects:** [X] (documented)

## Quality Metrics
- **Test Coverage:** [X%]
- **Code Coverage:** [X%] (if applicable)
- **Performance:** [Within/Outside] acceptable range
- **Security Scan:** [Passed/Failed]

## Risks & Mitigations
[List any outstanding risks and mitigation plans]

## Deployment Plan
- **Deployment Strategy:** [Blue-Green/Rolling/Canary/All-at-Once]
- **Deployment Window:** [Date/Time]
- **Rollback Plan:** [Documented/Tested]

## Recommendations
☐ **GO** - All criteria met, ready for production deployment
☐ **NO-GO** - Issues identified, deployment blocked

**Reason (if NO-GO):** [Explanation]

## Sign-off

| Role | Name | Approve/Reject | Date |
|------|------|----------------|------|
| **QA Lead** | [Name] | ☐ Approve ☐ Reject | [Date] |
| **Dev Lead** | [Name] | ☐ Approve ☐ Reject | [Date] |
| **Product Owner** | [Name] | ☐ Approve ☐ Reject | [Date] |
| **Release Manager** | [Name] | ☐ Approve ☐ Reject | [Date] |

**Final Decision:** ☐ GO / ☐ NO-GO

**Signed By:** _________________ **Date:** _________
```

---

## Appendix

### Appendix A: Quick Reference Commands

#### Environment Setup
```powershell
# Start Docker containers
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose up -d

# Health check
curl http://localhost:8001/api/health
curl http://localhost:8085
```

#### Test Execution
```powershell
# Navigate to test directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"

# Run all tests
python -m pytest -v --tb=short --html=report.html --self-contained-html

# Run smoke tests only
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow -v --tb=short

# Run specific category
python -m pytest Tests/test_backend_api.py -v --tb=short
```

---

### Appendix B: Troubleshooting Guide

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Common Issues:**

1. **Docker containers not running**
   - Solution: `docker-compose up -d`

2. **Tests fail with connection errors**
   - Solution: Verify services running, check health endpoints

3. **Addressable API rate limit exceeded**
   - Solution: Wait 24 hours or use VPN to change IP

4. **AWS Cognito authentication fails**
   - Solution: Verify user exists, check credentials in config

---

### Appendix C: Glossary

| Term | Definition |
|------|------------|
| **API** | Application Programming Interface |
| **AWS Cognito** | Amazon Web Services authentication service |
| **Addressable API** | Third-party NZ address autocomplete service |
| **Contract Testing** | Testing to verify external API schema compliance |
| **Docker** | Containerization platform |
| **E2E Testing** | End-to-end testing of complete user workflows |
| **JWT** | JSON Web Token (authentication token format) |
| **Page Object Model** | Design pattern for UI test abstraction |
| **Playwright** | Browser automation framework |
| **Pytest** | Python testing framework |
| **Regression Testing** | Re-running tests to ensure existing functionality works |
| **Smoke Testing** | Quick validation of critical functionality |

---

### Appendix D: Contact Information

| Role | Responsibility | Contact |
|------|---------------|---------|
| **QA Lead** | Test planning, sign-off | [Email] |
| **Test Engineer 1** | Test execution, automation | [Email] |
| **Test Engineer 2** | Test case development | [Email] |
| **DevOps Engineer** | Environment management | [Email] |
| **Development Lead** | Code fixes, architecture | [Email] |
| **Product Owner** | Requirements, priorities | [Email] |

---

### Appendix E: Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| [README](../README.md) | Root directory | Project overview |
| [Quick Start Guide](QUICK_START.md) | Documents/ | 5-minute setup guide |
| [Test Cases](TEST_CASES.md) | Documents/ | Detailed test specifications |
| [Test Strategy](TEST_STRATEGY.md) | Documents/ | Testing approach |
| [Impact Analysis](IMPACT_ANALYSIS.md) | Documents/ | Change impact assessment |
| [Architecture Guide](ARCHITECTURE.md) | Documents/ | Technical architecture |
| [Troubleshooting Guide](TROUBLESHOOTING.md) | Documents/ | Common issues and fixes |

---

**End of Test Plan Document**

---

**Document Control:**
- **Created:** April 22, 2026
- **Last Updated:** April 22, 2026
- **Next Review:** July 22, 2026 (Quarterly)
- **Version:** 1.0
- **Status:** ✅ Approved and Active
