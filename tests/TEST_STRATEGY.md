# Test Strategy - NZ Address Checker Application

## 1. Overview

This document outlines the comprehensive testing strategy for the NZ Address Checker application. The testing approach combines end-to-end (E2E) automation, integration testing, and visual validation to ensure application reliability and quality.

## 2. Scope

### In Scope
- **Frontend Testing**: React UI components, user interactions, form validation
- **Authentication**: AWS Cognito login/logout flows, token validation
- **API Integration**: Address suggestion and validation endpoints
- **User Workflows**: Complete end-to-end flows from login to address validation
- **Visual Testing**: UI appearance, responsive design, error states
- **Data Validation**: Correct address data processing and display

### Out of Scope
- Backend unit tests (handled by pytest)
- Infrastructure testing
- Load/performance testing (future phase)
- Security penetration testing

## 3. Testing Framework

### Technology Stack
- **Automation Tool**: Playwright (Python)
- **Test Runner**: pytest
- **Reporting**: Pytest HTML Reports + Custom Dashboard
- **Visual Monitoring**: Playwright built-in screenshots/videos
- **CI/CD Integration**: GitHub Actions

### Why Playwright?
- Cross-browser support (Chrome, Firefox, Safari)
- Native Python support
- Built-in visual debugging and recording
- Reliable waits and synchronization
- Excellent for E2E testing complex SPAs

## 4. Test Levels

### Level 1: Authentication Tests
- Login with valid credentials
- Login with invalid credentials
- Logout functionality
- Token refresh and expiration

### Level 2: Core Functionality Tests
- Address suggestions API
- Address validation API
- Error handling and edge cases
- Cognito token validation errors

### Level 3: User Journey Tests
- Complete login → suggest address → validate address → logout flow
- Error recovery workflows
- Session timeout handling

### Level 4: Visual & UI Tests
- Form validation feedback
- Error message display
- Responsive design verification
- Loading states and animations

## 5. Test Execution Strategy

### Local Execution
```bash
# Run all tests
pytest tests/ -v

# Run with browser visible
pytest tests/ -v --headed

# Run with video recording
pytest tests/ -v --video=on

# Run single test file
pytest tests/test_auth.py -v
```

### CI/CD Execution
- Tests run automatically on push to `practice` and `main` branches
- Results published to HTML report
- Screenshots/videos attached on failure
- GitHub Actions integration

## 6. Test Data Management

### Test Users
- **Valid User**: Email/password from AWS Cognito test account
- **Invalid User**: Non-existent credentials for negative testing
- **Expired Token**: Simulated token expiration scenarios

### Test Addresses
- **Valid NZ Address**: Full address in NZ Post database
- **Invalid Address**: Non-existent address for error testing
- **Partial Address**: Address suggestion testing
- **Edge Cases**: Special characters, very long strings, empty input

## 7. Reporting & Metrics

### Test Reports
- HTML report with screenshots
- Test execution summary (Pass/Fail/Skip)
- Execution time tracking
- Screenshots on failure
- Video recordings on failure

### Success Metrics
- Test Pass Rate: Target 95%+
- Test Execution Time: Under 5 minutes for full suite
- Coverage: All critical user workflows

## 8. Maintenance & Updates

### Test Maintenance
- Review tests monthly for flakiness
- Update tests when UI/API changes
- Keep test data current with application state
- Archive old test results (30+ days)

### Test Review Process
1. Code review for new tests
2. Peer review before merging
3. Regular sanity checks (weekly)
4. Quarterly test strategy review

## 9. Risk Management

### Known Risks
- **Flaky Tests**: May occur with slow network or timeouts
  - Mitigation: Explicit waits, retry logic
- **Cognito Rate Limiting**: Could block tests during heavy execution
  - Mitigation: Test user pool dedicated to automation, staggered execution
- **External Service Dependencies**: NZ Post API availability
  - Mitigation: Mock responses when needed, fallback scenarios

## 10. Future Enhancements

- [ ] Performance testing integration
- [ ] Accessibility (A11y) testing
- [ ] Cross-browser testing matrix
- [ ] Visual regression testing
- [ ] Load testing and stress testing
- [ ] Mobile device testing

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19  
**Author**: Copilot & Team
