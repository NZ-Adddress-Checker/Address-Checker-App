# Test Plan - NZ Address Checker Application

## 1. Introduction

This test plan documents the detailed approach for testing the NZ Address Checker application using Playwright and Python. It includes test scope, schedule, resource requirements, and deliverables.

## 2. Objectives

- Verify all critical user workflows function correctly
- Ensure Cognito authentication integration works reliably
- Validate address suggestion and validation APIs
- Detect regressions early through automated testing
- Provide continuous feedback on application quality

## 3. Test Scope

### Features Under Test
1. **Authentication**
   - User login via Cognito
   - User logout
   - Session management
   - Token validation

2. **Address Management**
   - Address suggestions (autocomplete)
   - Address validation
   - Error handling for invalid addresses
   - Data persistence

3. **User Interface**
   - Form validation and feedback
   - Error message display
   - Navigation between pages
   - Loading indicators

4. **Integration**
   - Cognito JWT token validation
   - NZ Post API integration
   - CORS handling
   - Error recovery

### Out of Scope
- Performance testing
- Load testing
- Security penetration testing
- Backend unit tests
- Infrastructure provisioning

## 4. Test Schedule

### Phase 1: Setup & Infrastructure (Week 1)
- [ ] Install Playwright and dependencies
- [ ] Set up test environment and fixtures
- [ ] Create test data management
- [ ] Set up CI/CD integration

### Phase 2: Authentication Tests (Week 2)
- [ ] Login functionality
- [ ] Logout functionality
- [ ] Error handling
- [ ] Token validation

### Phase 3: Core Functionality Tests (Week 3)
- [ ] Address suggestions
- [ ] Address validation
- [ ] Error scenarios
- [ ] Edge cases

### Phase 4: User Journey Tests (Week 4)
- [ ] Complete workflows
- [ ] Navigation flows
- [ ] Session management
- [ ] Error recovery

### Phase 5: Visual & Polish (Week 5)
- [ ] Visual regression tests
- [ ] Responsive design verification
- [ ] Accessibility checks (basic)
- [ ] Performance baseline

### Phase 6: Maintenance & Documentation (Ongoing)
- [ ] Test maintenance
- [ ] Report generation
- [ ] Documentation updates
- [ ] Test optimization

## 5. Test Organization

### Test Directory Structure
```
tests/
├── conftest.py                 # Pytest fixtures and configuration
├── test_data.py               # Test data and utilities
├── auth/
│   ├── test_login.py          # Login test cases
│   ├── test_logout.py         # Logout test cases
│   └── test_token.py          # Token validation tests
├── address/
│   ├── test_suggestions.py    # Address suggestion tests
│   ├── test_validation.py     # Address validation tests
│   └── test_errors.py         # Error handling tests
├── workflows/
│   └── test_user_journeys.py  # End-to-end workflows
├── visual/
│   └── test_ui_elements.py    # Visual verification tests
└── reports/                    # Test results and reports
```

## 6. Test Environment

### Development Environment
- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:8000
- **Browser**: Chromium (default)
- **Headless Mode**: False (show browser during test)

### CI/CD Environment
- **Browser**: Chromium
- **Headless Mode**: True
- **Video Recording**: On failure
- **Screenshots**: On failure

### Test Configuration
```python
# Base URL
BASE_URL = "http://localhost:8080"
API_URL = "http://localhost:8000"

# Cognito Configuration
COGNITO_DOMAIN = "ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com"
COGNITO_CLIENT_ID = "4p7i1nq2t426jufkh0pe7fgo2u"

# Timeouts
TIMEOUT_MS = 10000  # 10 seconds
WAIT_TIMEOUT_MS = 15000  # 15 seconds
```

## 7. Resource Requirements

### Tools & Libraries
- Python 3.12+
- Playwright
- pytest
- pytest-html (reporting)
- python-dotenv (environment variables)

### Test Data
- AWS Cognito test user account
- NZ Address test dataset
- Mock/stub responses for external services

### Infrastructure
- Test database (if needed)
- CI/CD runner (GitHub Actions)
- Report storage (GitHub Pages)

## 8. Test Deliverables

### Test Artifacts
1. **Test Code**
   - Automated test scripts (Python)
   - Test fixtures and utilities
   - Page Object Models (POMs)

2. **Test Reports**
   - HTML test execution reports
   - Screenshots and videos
   - Test metrics and statistics

3. **Documentation**
   - Test Strategy (this document)
   - Test Plan (this document)
   - Test Scenarios
   - Detailed Test Cases
   - Test Execution Guide

4. **Configuration Files**
   - pytest.ini
   - conftest.py
   - Environment configuration

## 9. Entry & Exit Criteria

### Entry Criteria
- [ ] Application deployed and running
- [ ] Cognito configured and test users created
- [ ] Test environment accessible
- [ ] Development tools installed

### Exit Criteria
- [ ] All planned test cases executed
- [ ] Pass rate ≥ 95%
- [ ] All critical defects resolved
- [ ] Test reports generated and reviewed
- [ ] Documentation complete

## 10. Risk Management

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Flaky tests due to timing | High | Medium | Use explicit waits, retry logic |
| Cognito rate limits | Medium | High | Dedicated test account, staggered runs |
| External API unavailability | Low | High | Mock responses, fallback tests |
| Browser compatibility issues | Low | Medium | Test on multiple browsers |

## 11. Metrics & Reporting

### Key Metrics
- **Test Execution Rate**: % of tests executed
- **Pass Rate**: % of tests that pass
- **Defect Density**: Defects found per test
- **Test Coverage**: User workflows covered
- **Execution Time**: Total time for all tests

### Report Generation
- Automated HTML reports after each test run
- Email notifications for failures
- Dashboard for trend analysis
- Weekly test summary

## 12. Approval & Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| QA Lead | - | - | - |
| Dev Lead | - | - | - |
| Product Owner | - | - | - |

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19  
**Next Review**: 2026-05-19
