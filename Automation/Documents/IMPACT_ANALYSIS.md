# Impact Analysis Document
**NZ Address Checker Application**

**Version:** 1.0  
**Last Updated:** April 22, 2026  
**Document Owner:** QA Team

---

## Table of Contents
1. [Document Purpose](#document-purpose)
2. [System Overview](#system-overview)
3. [Component Dependency Map](#component-dependency-map)
4. [Impact Assessment Matrix](#impact-assessment-matrix)
5. [Change Scenarios & Testing Impact](#change-scenarios--testing-impact)
6. [Risk Analysis](#risk-analysis)
7. [Test Coverage Mapping](#test-coverage-mapping)
8. [Deployment Impact](#deployment-impact)
9. [Rollback Procedures](#rollback-procedures)

---

## Document Purpose

This document provides comprehensive impact analysis for the NZ Address Checker application, enabling teams to:

- **Assess Change Impact**: Understand which components are affected by specific changes
- **Determine Test Scope**: Identify which tests must run for different change types
- **Evaluate Risk**: Assess risk levels for various modifications
- **Plan Deployments**: Make informed decisions about deployment strategies
- **Enable Quick Rollback**: Understand rollback implications and procedures

---

## System Overview

### Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                        End User                              │
└────────────────────┬────────────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   React Frontend    │
          │   (Port 8085)       │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │   FastAPI Backend   │
          │   (Port 8001)       │
          └──────┬───────┬──────┘
                 │       │
    ┌────────────▼─┐   ┌─▼─────────────────┐
    │ AWS Cognito  │   │ Addressable API   │
    │ (Auth)       │   │ (Address Data)    │
    └──────────────┘   └───────────────────┘
```

### Technology Stack

| Layer | Technology | Version | Port |
|-------|-----------|---------|------|
| Frontend | React | 18.x | 8085 |
| Backend | FastAPI | Latest | 8001 |
| Authentication | AWS Cognito | - | ap-southeast-2 |
| Address Data | Addressable API | v2 | HTTPS |
| Test Framework | Playwright + Pytest | 1.47.0 / 8.4.2 | - |
| Container Platform | Docker Compose | Latest | - |

### Critical Dependencies

1. **AWS Cognito** (ap-southeast-2_2oQQDAKa4)
   - User authentication
   - Token generation and validation
   - Session management

2. **Addressable API** (api.addressable.dev)
   - Address autocomplete
   - Address validation
   - API Key: A_xWMNLslywtPO2DQ8jiMg
   - Rate Limit: 100 requests/day (IP-based)

3. **Docker Containers**
   - Frontend container (React)
   - Backend container (FastAPI)

---

## Component Dependency Map

### Frontend Dependencies

```
React Frontend
├── Authentication Module
│   ├── AWS Cognito Client
│   ├── Token Storage (localStorage)
│   └── Login/Logout UI
├── Address Search Module
│   ├── Backend API Client (/api/address/suggest)
│   ├── Dropdown Component
│   └── Input Validation
├── Address Validation Module
│   ├── Backend API Client (/api/address/validate)
│   └── Results Display
└── Error Handling Module
    ├── Network Error Detection
    ├── Timeout Handling
    └── Error Message Display
```

**Impacted By:**
- Backend API endpoint changes
- AWS Cognito configuration changes
- Token format modifications
- Error response structure changes

**Impacts:**
- User experience
- Session management
- API request patterns
- Error recovery behavior

---

### Backend Dependencies

```
FastAPI Backend
├── Authentication Middleware
│   ├── JWT Token Validation
│   ├── Bearer Token Extraction
│   └── AWS Cognito Integration
├── Address Suggest Endpoint (/api/address/suggest)
│   ├── Addressable API Client
│   ├── Query Parameter Validation
│   └── Response Transformation
├── Address Validate Endpoint (/api/address/validate)
│   ├── Addressable API Client
│   ├── Request Body Validation
│   └── Validation Logic
└── Health Check Endpoint (/api/health)
    └── Service Status Monitoring
```

**Impacted By:**
- Addressable API changes
- AWS Cognito JWT structure changes
- Frontend request format changes
- Rate limit modifications

**Impacts:**
- Frontend functionality
- Authentication flow
- Address data quality
- API response times

---

### External Service Dependencies

#### AWS Cognito

**Service Details:**
- Pool ID: ap-southeast-2_2oQQDAKa4
- Client ID: 4p7i1nq2t426jufkh0pe7fgo2u
- Region: ap-southeast-2

**Dependency Type:** Critical - System Non-Functional Without It

**Change Impact:**
- User pool configuration → HIGH IMPACT (all authentication fails)
- JWT token format → HIGH IMPACT (all API requests fail)
- Client ID/Secret → HIGH IMPACT (login fails)
- User attributes → MEDIUM IMPACT (user data display)

**Testing Required:**
- TC-001, TC-003, TC-004 (Functional - Login/Logout)
- TC-005 to TC-010 (All Security Tests)
- TC-011 to TC-013 (All API Auth Tests)

---

#### Addressable API

**Service Details:**
- Endpoint: https://api.addressable.dev/v2/autocomplete
- API Key: A_xWMNLslywtPO2DQ8jiMg
- Rate Limit: 100 requests/day (IP-based)

**Dependency Type:** Critical - Core Feature Non-Functional Without It

**Change Impact:**
- API endpoint URL → HIGH IMPACT (all address features fail)
- Response schema → HIGH IMPACT (data parsing fails)
- API key → HIGH IMPACT (all requests rejected)
- Rate limits → MEDIUM IMPACT (usage patterns affected)

**Testing Required:**
- TC-001, TC-002 (Functional - Address Flow)
- TC-014, TC-015, TC-016 (Error Handling)
- TC-017, TC-018, TC-019 (External API Contract)

---

## Impact Assessment Matrix

### Change Type vs System Impact

| Change Area | Frontend | Backend | Auth | External API | Database | Test Scope |
|-------------|----------|---------|------|--------------|----------|------------|
| **UI Components** | 🔴 High | 🟢 None | 🟢 None | 🟢 None | 🟢 None | Functional (4) |
| **Authentication Flow** | 🔴 High | 🔴 High | 🔴 High | 🟢 None | 🟢 None | Security (6), Functional (4) |
| **API Endpoints** | 🟡 Medium | 🔴 High | 🟡 Medium | 🟡 Medium | 🟢 None | API (3), Functional (2) |
| **Address Suggest** | 🟡 Medium | 🔴 High | 🟢 None | 🔴 High | 🟢 None | Functional (2), Contract (3) |
| **Address Validate** | 🟡 Medium | 🔴 High | 🟢 None | 🔴 High | 🟢 None | Functional (2), Contract (3) |
| **JWT Security** | 🟡 Medium | 🔴 High | 🔴 High | 🟢 None | 🟢 None | Security (6), API (3) |
| **Error Handling** | 🔴 High | 🟡 Medium | 🟢 None | 🟡 Medium | 🟢 None | Error (3), Functional (1) |
| **Docker Configuration** | 🔴 High | 🔴 High | 🟢 None | 🟢 None | 🟢 None | Full Suite (19) |
| **Environment Variables** | 🟡 Medium | 🔴 High | 🔴 High | 🔴 High | 🟢 None | Full Suite (19) |
| **Rate Limiting** | 🟡 Medium | 🟡 Medium | 🟢 None | 🔴 High | 🟢 None | Contract (3), Error (3) |

**Legend:**
- 🔴 High Impact: Direct functional impact, immediate testing required
- 🟡 Medium Impact: Indirect impact, selective testing required
- 🟢 None/Low Impact: No significant impact, smoke testing sufficient

---

## Change Scenarios & Testing Impact

### Scenario 1: Frontend UI Component Changes

**Example Changes:**
- Button text/styling modifications
- Layout adjustments
- Color scheme updates
- Icon changes

**Impact Level:** 🟡 MEDIUM

**Affected Components:**
- React Frontend (High)
- User Experience (Medium)

**Testing Required:**

| Test ID | Test Name | Priority | Reason |
|---------|-----------|----------|--------|
| TC-001 | Valid User Complete Flow | Critical | Verify end-to-end functionality |
| TC-002 | Validation Requires Dropdown | High | Verify UI interactions |
| TC-004 | User Logout | Medium | Verify UI navigation |

**Deployment Strategy:** Blue-Green or Rolling Update  
**Rollback Complexity:** Low (frontend only)  
**Estimated Testing Time:** 15-20 minutes

---

### Scenario 2: Authentication/JWT Changes

**Example Changes:**
- JWT token structure modifications
- Cognito user pool configuration
- Token expiration time changes
- Bearer token prefix requirements

**Impact Level:** 🔴 HIGH

**Affected Components:**
- Frontend Auth Module (High)
- Backend Auth Middleware (High)
- AWS Cognito Integration (High)
- All API Endpoints (High)

**Testing Required:**

| Test ID | Test Name | Priority | Reason |
|---------|-----------|----------|--------|
| TC-001 | Valid User Complete Flow | Critical | Verify authentication works |
| TC-003 | Invalid User Access Blocked | Critical | Verify auth rejection |
| TC-004 | User Logout | Critical | Verify session termination |
| TC-005 | Suggest Endpoint Requires Auth | Critical | Verify API protection |
| TC-006 | Validate Endpoint Requires Auth | Critical | Verify API protection |
| TC-007 | Invalid Token Rejected | Critical | Verify token validation |
| TC-008 | Tampered JWT Rejected | Critical | Verify JWT integrity |
| TC-009 | No Bearer Prefix Rejected | Critical | Verify token format |
| TC-010 | Empty Token Rejected | Critical | Verify token presence |
| TC-011 | Validate Without Auth (401) | High | Verify error responses |
| TC-012 | Suggest Without Auth (401) | High | Verify error responses |

**Deployment Strategy:** Staged Rollout with Immediate Rollback Plan  
**Rollback Complexity:** High (requires coordinated frontend/backend rollback)  
**Estimated Testing Time:** 45-60 minutes  
**Pre-Deployment:** Test in staging with real Cognito integration

---

### Scenario 3: Backend API Endpoint Modifications

**Example Changes:**
- New query parameters
- Response structure changes
- Endpoint URL changes
- Request/response validation rules

**Impact Level:** 🔴 HIGH

**Affected Components:**
- Backend API Handlers (High)
- Frontend API Client (Medium)
- Addressable API Integration (Medium)

**Testing Required:**

| Test ID | Test Name | Priority | Reason |
|---------|-----------|----------|--------|
| TC-001 | Valid User Complete Flow | Critical | Verify integration works |
| TC-002 | Validation Requires Dropdown | Critical | Verify suggest flow |
| TC-005 | Suggest Endpoint Requires Auth | Critical | Verify suggest endpoint |
| TC-006 | Validate Endpoint Requires Auth | Critical | Verify validate endpoint |
| TC-011 | Validate Without Auth (401) | High | Verify auth enforcement |
| TC-012 | Suggest Without Auth (401) | High | Verify auth enforcement |
| TC-013 | Validate Missing Field (422) | High | Verify validation logic |
| TC-014 | API Timeout Shows Error | High | Verify error handling |
| TC-015 | Slow API Response Handling | High | Verify performance |
| TC-016 | Network Error Recovery | High | Verify resilience |

**Deployment Strategy:** Blue-Green Deployment  
**Rollback Complexity:** Medium (backend rollback may affect in-flight requests)  
**Estimated Testing Time:** 35-45 minutes  
**API Contract Validation:** Essential before deployment

---

### Scenario 4: Addressable API Integration Changes

**Example Changes:**
- API endpoint URL update
- API key rotation
- Response schema changes
- Rate limit adjustments

**Impact Level:** 🔴 HIGH

**Affected Components:**
- Backend Addressable Client (High)
- Address Suggest Function (High)
- Address Validate Function (High)
- Frontend Results Display (Medium)

**Testing Required:**

| Test ID | Test Name | Priority | Reason |
|---------|-----------|----------|--------|
| TC-001 | Valid User Complete Flow | Critical | Verify address search works |
| TC-002 | Validation Requires Dropdown | Critical | Verify suggestion flow |
| TC-014 | API Timeout Shows Error | High | Verify timeout handling |
| TC-015 | Slow API Response Handling | High | Verify slow response |
| TC-016 | Network Error Recovery | High | Verify recovery logic |
| TC-017 | Addressable Returns List | Critical | Verify contract compliance |
| TC-018 | Addressable Items Have Formatted | Critical | Verify schema compliance |
| TC-019 | Addressable Schema Validation | Critical | Verify data structure |

**Deployment Strategy:** Canary Deployment (5% → 25% → 100%)  
**Rollback Complexity:** Medium (config change only)  
**Estimated Testing Time:** 40-50 minutes  
**Contract Testing:** Run TC-017 to TC-019 on STAGING first

---

### Scenario 5: Error Handling & Network Resilience

**Example Changes:**
- Timeout duration adjustments
- Error message text changes
- Retry logic modifications
- Fallback behavior changes

**Impact Level:** 🟡 MEDIUM

**Affected Components:**
- Frontend Error Handler (High)
- Backend Error Responses (Medium)
- User Notifications (Medium)

**Testing Required:**

| Test ID | Test Name | Priority | Reason |
|---------|-----------|----------|--------|
| TC-014 | API Timeout Shows Error | Critical | Verify timeout detection |
| TC-015 | Slow API Response Handling | Critical | Verify UI responsiveness |
| TC-016 | Network Error Recovery | Critical | Verify recovery works |
| TC-001 | Valid User Complete Flow | High | Verify normal flow unaffected |

**Deployment Strategy:** Rolling Update  
**Rollback Complexity:** Low  
**Estimated Testing Time:** 20-25 minutes

---

### Scenario 6: Docker/Infrastructure Changes

**Example Changes:**
- Docker base image updates
- Environment variable changes
- Port modifications
- Container resource limits

**Impact Level:** 🔴 HIGH

**Affected Components:**
- Entire Application Stack (High)
- Service Availability (High)
- Performance Characteristics (Medium)

**Testing Required:**

| Category | Test Count | Reason |
|----------|------------|--------|
| Full Test Suite | 19 tests | Verify complete system functionality |
| Functional Tests | 4 tests | Verify core user flows |
| Security Tests | 6 tests | Verify auth still works |
| API Tests | 3 tests | Verify endpoints accessible |
| Error Handling | 3 tests | Verify resilience maintained |
| Contract Tests | 3 tests | Verify external integration |

**Deployment Strategy:** Blue-Green with Extended Monitoring  
**Rollback Complexity:** High (infrastructure level)  
**Estimated Testing Time:** 90-120 minutes (full regression)  
**Health Checks:** Monitor /api/health endpoint continuously

---

### Scenario 7: Environment Configuration Changes

**Example Changes:**
- AWS Cognito pool/client IDs
- Addressable API key rotation
- CORS settings
- Logging levels

**Impact Level:** 🔴 HIGH

**Affected Components:**
- Authentication (High if Cognito)
- External API Access (High if Addressable)
- Cross-Origin Requests (High if CORS)

**Testing Required:**

**If Cognito Config Changed:**
- All Security Tests (TC-005 to TC-010)
- All Functional Tests (TC-001 to TC-004)

**If Addressable API Config Changed:**
- All Contract Tests (TC-017 to TC-019)
- Functional Address Tests (TC-001, TC-002)

**If CORS Changed:**
- Full Frontend Integration Tests

**Deployment Strategy:** Configuration-Only Deployment  
**Rollback Complexity:** Low (config revert only)  
**Estimated Testing Time:** 30-60 minutes (depends on scope)

---

## Risk Analysis

### High-Risk Change Categories

#### 1. Authentication & Security (Risk Level: 🔴 CRITICAL)

**Why High Risk:**
- Affects ALL users immediately
- Security vulnerability potential
- Session invalidation can lock out users
- Complex rollback requirements

**Mitigation Strategies:**
- Test on staging with real Cognito integration
- Maintain backward compatibility for 24 hours
- Deploy during low-traffic periods
- Have immediate rollback plan ready
- Monitor authentication failure rates in real-time

**Test Coverage Required:** 100% of Security Tests (TC-005 to TC-010)  
**Rollback Time Target:** < 5 minutes  
**Monitoring Duration:** 72 hours post-deployment

---

#### 2. External API Integration (Risk Level: 🔴 HIGH)

**Why High Risk:**
- Third-party dependency (Addressable)
- Rate limit implications
- Data contract changes can break parsing
- No control over external service availability

**Mitigation Strategies:**
- Validate contract on staging first (TC-017 to TC-019)
- Implement graceful degradation
- Cache last working configuration
- Monitor error rates closely
- Have fallback API key ready

**Test Coverage Required:** 100% of Contract Tests (TC-017 to TC-019)  
**Rollback Time Target:** < 10 minutes  
**Monitoring Duration:** 48 hours post-deployment

---

#### 3. Infrastructure Changes (Risk Level: 🔴 HIGH)

**Why High Risk:**
- Affects entire application stack
- Potential downtime during deployment
- Performance characteristics may change
- Database connectivity issues possible

**Mitigation Strategies:**
- Blue-green deployment
- Full regression testing
- Performance baseline comparison
- Extended health monitoring
- Immediate rollback capability

**Test Coverage Required:** Full Test Suite (all 19 tests)  
**Rollback Time Target:** < 15 minutes  
**Monitoring Duration:** 7 days post-deployment

---

### Medium-Risk Change Categories

#### 4. API Endpoint Changes (Risk Level: 🟡 MEDIUM)

**Why Medium Risk:**
- Requires frontend/backend coordination
- Can break existing functionality
- Version management complexity

**Mitigation Strategies:**
- Maintain API versioning
- Test frontend/backend integration thoroughly
- Deploy backend first, frontend second
- Monitor API error rates

**Test Coverage Required:** API Tests + Functional Tests (10 tests)  
**Rollback Time Target:** < 10 minutes

---

#### 5. UI/UX Changes (Risk Level: 🟡 MEDIUM)

**Why Medium Risk:**
- User experience impact
- Potential accessibility issues
- Workflow disruption

**Mitigation Strategies:**
- A/B testing capability
- User acceptance testing
- Accessibility validation
- Gradual rollout (canary)

**Test Coverage Required:** Functional Tests (TC-001 to TC-004)  
**Rollback Time Target:** < 5 minutes

---

### Low-Risk Change Categories

#### 6. Logging & Monitoring (Risk Level: 🟢 LOW)

**Mitigation:** Smoke testing only  
**Test Coverage:** Health check validation

#### 7. Documentation Updates (Risk Level: 🟢 LOW)

**Mitigation:** Peer review  
**Test Coverage:** None required

---

## Test Coverage Mapping

### Component → Test Mapping

#### Frontend Components

| Component | Test IDs | Coverage % | Critical Tests |
|-----------|----------|------------|----------------|
| Login Module | TC-001, TC-003, TC-004 | 100% | TC-001, TC-003 |
| Address Input | TC-001, TC-002 | 100% | TC-001, TC-002 |
| Dropdown Selection | TC-002 | 100% | TC-002 |
| Validation Display | TC-001, TC-002 | 100% | TC-001 |
| Error Messages | TC-014, TC-015, TC-016 | 100% | TC-014, TC-016 |
| Logout Functionality | TC-004 | 100% | TC-004 |

**Total Frontend Coverage:** 100% (all user flows tested)

---

#### Backend Endpoints

| Endpoint | Test IDs | Coverage % | Critical Tests |
|----------|----------|------------|----------------|
| /api/address/suggest | TC-001, TC-002, TC-005, TC-012 | 100% | TC-001, TC-005 |
| /api/address/validate | TC-001, TC-002, TC-006, TC-011, TC-013 | 100% | TC-001, TC-006 |
| Authentication Middleware | TC-005 to TC-013 | 100% | TC-007, TC-008 |
| Health Check | Manual | - | - |

**Total Backend Coverage:** 100% (all endpoints tested)

---

#### Security Mechanisms

| Security Feature | Test IDs | Coverage % | Critical Tests |
|------------------|----------|------------|----------------|
| JWT Validation | TC-007, TC-008, TC-009, TC-010 | 100% | TC-007, TC-008 |
| Bearer Token | TC-009, TC-010 | 100% | TC-009 |
| Auth Enforcement | TC-005, TC-006, TC-011, TC-012 | 100% | TC-005, TC-006 |
| Access Control | TC-003 | 100% | TC-003 |
| Token Rejection | TC-007, TC-008, TC-009, TC-010 | 100% | All |

**Total Security Coverage:** 100% (all security vectors tested)

---

#### External Integrations

| Integration | Test IDs | Coverage % | Critical Tests |
|-------------|----------|------------|----------------|
| AWS Cognito | TC-001, TC-003, TC-004 | 100% | TC-001, TC-003 |
| Addressable API | TC-017, TC-018, TC-019 | 100% | TC-017, TC-018 |
| Error Recovery | TC-014, TC-015, TC-016 | 100% | TC-014, TC-016 |

**Total Integration Coverage:** 100% (all integrations tested)

---

### Test Priority Matrix

#### Priority 1 - Critical (Must Pass Before Deployment)

| Test ID | Component Covered | Failure Impact |
|---------|-------------------|----------------|
| TC-001 | Complete User Flow | System unusable |
| TC-003 | Access Control | Security breach |
| TC-005 | API Auth (Suggest) | Feature broken |
| TC-006 | API Auth (Validate) | Feature broken |
| TC-007 | Token Validation | Security breach |
| TC-008 | JWT Integrity | Security breach |
| TC-017 | Addressable Contract | External API broken |

**Total Critical Tests:** 7  
**Must-Pass Rate:** 100% required for production deployment

---

#### Priority 2 - High (Should Pass Before Deployment)

| Test ID | Component Covered | Failure Impact |
|---------|-------------------|----------------|
| TC-002 | Dropdown Validation | UX degradation |
| TC-004 | Logout | Session issues |
| TC-009 | Bearer Prefix | Auth edge case |
| TC-010 | Empty Token | Auth edge case |
| TC-011 | Validate Auth 401 | Error handling |
| TC-012 | Suggest Auth 401 | Error handling |
| TC-014 | Timeout Handling | Error UX |
| TC-016 | Error Recovery | Resilience |
| TC-018 | Addressable Schema | Data quality |

**Total High Tests:** 9  
**Target Pass Rate:** ≥ 95%

---

#### Priority 3 - Medium (Nice to Pass)

| Test ID | Component Covered | Failure Impact |
|---------|-------------------|----------------|
| TC-013 | Validate 422 Error | Edge case |
| TC-015 | Slow Response | Performance |
| TC-019 | Addressable Schema Validation | Data validation |

**Total Medium Tests:** 3  
**Target Pass Rate:** ≥ 80%

---

### Change Type → Required Tests

| Change Type | Minimum Tests | Recommended Full Coverage |
|-------------|---------------|---------------------------|
| Frontend Only | TC-001, TC-002, TC-004 | All Functional (4) |
| Backend Only | TC-005, TC-006, TC-011, TC-012 | All API (3) + Functional (4) |
| Auth Changes | TC-001, TC-003, TC-005-010 | Security (6) + Functional (4) |
| External API | TC-001, TC-017, TC-018 | Contract (3) + Functional (2) + Error (3) |
| Infrastructure | All 19 Tests | All 19 Tests |
| Error Handling | TC-014, TC-015, TC-016 | Error (3) + Functional (1) |
| Security | TC-005 to TC-010 | Security (6) + API (3) + Functional (4) |

---

## Deployment Impact

### Deployment Strategy Recommendations

#### Blue-Green Deployment

**Best For:**
- Backend API changes
- Infrastructure updates
- High-risk deployments

**Process:**
1. Deploy new version to "green" environment
2. Run full test suite on green
3. Switch traffic to green
4. Monitor for 1 hour
5. Keep blue as instant rollback

**Testing Required:** Full regression (all 19 tests)  
**Downtime:** Zero  
**Rollback Time:** < 2 minutes (traffic switch)

---

#### Rolling Update

**Best For:**
- Frontend UI changes
- Low-risk updates
- Error handling improvements

**Process:**
1. Update 25% of instances
2. Run smoke tests (Priority 1 tests)
3. Update next 25%
4. Continue until 100%

**Testing Required:** Critical tests (7 tests)  
**Downtime:** Zero  
**Rollback Time:** 5-10 minutes (rolling back)

---

#### Canary Deployment

**Best For:**
- External API integration changes
- Feature releases
- Performance optimizations

**Process:**
1. Deploy to 5% of users
2. Monitor metrics for 2 hours
3. Expand to 25% if healthy
4. Expand to 100% if healthy

**Testing Required:** Full suite on canary (19 tests)  
**Downtime:** Zero  
**Rollback Time:** < 5 minutes (route traffic back)

---

#### All-at-Once (Big Bang)

**Best For:**
- Documentation updates
- Non-functional changes
- Emergency security patches

**Process:**
1. Deploy to all instances simultaneously
2. Monitor aggressively
3. Rollback if issues detected

**Testing Required:** Based on change type  
**Downtime:** Possible (2-5 minutes)  
**Rollback Time:** 10-15 minutes

---

### Pre-Deployment Checklist

#### For All Deployments

- [ ] All required tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Rollback plan documented
- [ ] Monitoring dashboards ready
- [ ] On-call engineer identified
- [ ] Deployment window scheduled

#### For High-Risk Deployments (Auth, Infrastructure, External API)

- [ ] Staging environment tested with production-like data
- [ ] Performance benchmarks recorded
- [ ] Security scan completed
- [ ] Backup verified and tested
- [ ] Rollback tested in staging
- [ ] Communication plan ready (user notifications)
- [ ] Post-deployment validation checklist prepared

#### For Security Changes

- [ ] Security team approval obtained
- [ ] Vulnerability scan completed
- [ ] All security tests passing (TC-005 to TC-010)
- [ ] Penetration testing completed (if major change)
- [ ] Compliance requirements verified

---

### Post-Deployment Validation

#### Immediate Validation (0-15 minutes)

```powershell
# Health Check
curl http://localhost:8001/api/health

# Frontend Accessibility
curl http://localhost:8085

# Authentication Test
# Run TC-001 (Valid User Complete Flow)
pytest Tests/test_ui_flow.py::test_valid_user_flow -v
```

**Expected Results:**
- Health endpoint returns 200
- Frontend loads successfully
- User can login and complete address search

---

#### Short-Term Validation (15-60 minutes)

Run critical test suite:
```powershell
pytest Tests/test_ui_flow.py Tests/test_backend_api.py -v --tb=short
```

**Monitor:**
- Error rates (should be < 1%)
- Response times (should be < 2s p95)
- Authentication success rate (should be > 99%)

---

#### Extended Validation (1-24 hours)

Run full regression:
```powershell
pytest -v --tb=short
```

**Monitor:**
- User session duration (no abnormal drops)
- API rate limit consumption (within expected range)
- Memory/CPU usage (stable)
- External API error rates (< 2%)

---

## Rollback Procedures

### Rollback Decision Criteria

**Immediate Rollback (< 5 minutes) If:**
- Authentication failure rate > 10%
- Critical test (Priority 1) fails
- System unavailable for > 2 minutes
- Security vulnerability detected
- External API integration broken (100% failure)

**Planned Rollback (< 30 minutes) If:**
- Error rate > 5% sustained for 10 minutes
- Performance degradation > 50%
- User complaints exceed threshold
- Data inconsistency detected

---

### Rollback Procedures by Component

#### Frontend Rollback

**Time Estimate:** 3-5 minutes

```powershell
# Navigate to app directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"

# Rollback frontend container to previous version
docker-compose down frontend
docker image ls | Select-String "frontend"  # Find previous image
docker tag address-checker-app_frontend:previous address-checker-app_frontend:latest
docker-compose up -d frontend

# Validate
curl http://localhost:8085
```

**Validation Tests:**
- TC-001: Valid User Complete Flow
- TC-002: Validation Requires Dropdown Selection

---

#### Backend Rollback

**Time Estimate:** 5-10 minutes

```powershell
# Navigate to app directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"

# Rollback backend container
docker-compose down backend
docker image ls | Select-String "backend"  # Find previous image
docker tag address-checker-app_backend:previous address-checker-app_backend:latest
docker-compose up -d backend

# Wait for startup
Start-Sleep -Seconds 5

# Validate
curl http://localhost:8001/api/health
```

**Validation Tests:**
- TC-005: Suggest Endpoint Requires Auth
- TC-006: Validate Endpoint Requires Auth
- TC-001: Valid User Complete Flow

---

#### Configuration Rollback

**Time Estimate:** 2-3 minutes

**For Environment Variables:**
```powershell
# Restore previous .env file
Copy-Item .env.backup .env -Force
docker-compose restart
```

**For AWS Cognito Config:**
1. Restore previous Pool ID in .env
2. Restore previous Client ID in .env
3. Restart backend container

**Validation Tests:**
- TC-001: Valid User Complete Flow
- TC-003: Invalid User Access Blocked
- All Security Tests (TC-005 to TC-010)

---

#### Full Stack Rollback

**Time Estimate:** 10-15 minutes

```powershell
# Complete rollback
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"

# Restore previous docker-compose.yml
Copy-Item docker-compose.yml.backup docker-compose.yml -Force

# Rebuild from previous commit
git checkout HEAD~1  # Or specific commit hash
docker-compose down
docker-compose up --build -d

# Validate all services
Start-Sleep -Seconds 10
curl http://localhost:8085
curl http://localhost:8001/api/health
```

**Validation Tests:**
- Full test suite (all 19 tests)
- Minimum: All Priority 1 tests (7 tests)

---

### Post-Rollback Actions

#### Immediate (0-15 minutes)

1. **Verify Services Running**
   ```powershell
   docker-compose ps
   curl http://localhost:8085
   curl http://localhost:8001/api/health
   ```

2. **Run Critical Tests**
   ```powershell
   cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"
   pytest Tests/test_ui_flow.py::test_valid_user_flow -v
   ```

3. **Monitor Error Rates**
   - Check application logs
   - Verify error rate < 1%
   - Confirm authentication working

---

#### Short-Term (15-60 minutes)

1. **Full Regression Test**
   ```powershell
   pytest -v --tb=short
   ```

2. **Document Failure**
   - Record what went wrong
   - Capture logs and error messages
   - Update impact analysis if needed

3. **Root Cause Analysis**
   - Identify why deployment failed
   - Determine what tests missed
   - Plan remediation

---

#### Long-Term (1-7 days)

1. **Post-Mortem Meeting**
   - Review failure timeline
   - Identify process improvements
   - Update deployment procedures

2. **Test Gap Analysis**
   - Identify missing test coverage
   - Create new test cases if needed
   - Update TEST_CASES.md

3. **Prevention Plan**
   - Implement additional safeguards
   - Enhance monitoring
   - Improve rollback automation

---

## Appendix

### Quick Reference - Test Execution Commands

```powershell
# Run all tests
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"
python -m pytest -v --tb=short

# Run critical tests only (Priority 1)
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow `
                Tests/test_ui_flow.py::test_invalid_user_blocked `
                Tests/test_backend_api.py::test_suggest_requires_auth `
                Tests/test_backend_api.py::test_validate_requires_auth `
                Tests/test_jwt_security.py::test_tampered_jwt_rejected `
                Tests/test_addressable_contract.py::test_addressable_returns_list `
                -v --tb=short

# Run functional tests
python -m pytest Tests/test_ui_flow.py -v --tb=short

# Run security tests
python -m pytest Tests/test_backend_api.py Tests/test_jwt_security.py Tests/test_address_api.py -v --tb=short

# Run error handling tests
python -m pytest Tests/test_error_handling.py -v --tb=short

# Generate HTML report
python -m pytest -v --tb=short --html=report.html --self-contained-html
```

---

### Contact Information

| Role | Contact | Responsibility |
|------|---------|----------------|
| QA Lead | - | Test execution approval |
| DevOps Engineer | - | Deployment execution |
| Backend Developer | - | Backend changes |
| Frontend Developer | - | Frontend changes |
| Security Team | - | Security approvals |
| Product Owner | - | Risk acceptance |

---

### Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | April 22, 2026 | QA Team | Initial creation with comprehensive impact analysis |

---

### Related Documentation

- [Test Cases](TEST_CASES.md) - Detailed test specifications
- [Test Strategy](TEST_STRATEGY.md) - Testing approach and methodology
- [Architecture Guide](ARCHITECTURE.md) - System architecture details
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [Quick Start Guide](QUICK_START.md) - Setup instructions

---

**End of Impact Analysis Document**
