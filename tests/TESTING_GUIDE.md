# Testing Guide - NZ Address Checker Application

## Quick Start

### Overview
This guide provides everything you need to understand the testing strategy, plan, scenarios, and test cases for the NZ Address Checker application.

### Documentation Files

1. **TEST_STRATEGY.md** (4.5 KB)
   - Testing approach and methodology
   - Framework and technology stack selection
   - Test levels (authentication, core functionality, journeys, visual)
   - Risk management
   - Future enhancements

2. **TEST_PLAN.md** (6.3 KB)
   - Detailed test plan with schedule
   - Test scope and objectives
   - Resource requirements
   - Test environment setup
   - Entry/exit criteria
   - Metrics and reporting strategy

3. **TEST_SCENARIOS.md** (11 KB)
   - 20+ comprehensive test scenarios
   - Organized by feature area
   - Preconditions and expected outcomes
   - Coverage of:
     - Authentication (login/logout/tokens)
     - Address suggestions
     - Address validation
     - Error handling
     - Complete user journeys
     - Visual & UI testing

4. **DETAILED_TEST_CASES.md** (15 KB)
   - 15 detailed test cases with full specification
   - Each test case includes:
     - Test ID and title
     - Category and priority
     - Preconditions
     - Test data specifications
     - Step-by-step execution instructions
     - Expected results and assertions
   - Test case summary table

### Test Case Coverage

| Area | Test Cases | Status |
|------|-----------|--------|
| Authentication | 4 | Documented |
| Address Suggestions | 3 | Documented |
| Address Validation | 4 | Documented |
| Error Handling | 2 | Documented |
| User Journeys | 2 | Documented |
| **Total** | **15** | **Ready for Implementation** |

### Test Priorities

| Priority | Count | Focus |
|----------|-------|-------|
| Critical | 7 | Core functionality, security |
| High | 5 | Important features |
| Medium | 3 | Nice-to-have features |

### Testing Framework

**Tool**: Playwright (Python)  
**Test Runner**: pytest  
**Reporting**: pytest-html + custom dashboard  
**Browser**: Chromium (primary), with support for Firefox, Safari  
**Headless Mode**: False (show browser during tests)  

### Implementation Roadmap

#### Phase 1: Setup (Week 1)
- [ ] Install Playwright and dependencies
- [ ] Create conftest.py with fixtures
- [ ] Create test data utilities (test_data.py)
- [ ] Set up CI/CD integration

#### Phase 2: Authentication Tests (Week 2)
- [ ] Implement TC-AUTH-001 through TC-AUTH-004
- [ ] Test login/logout workflows
- [ ] Verify token validation

#### Phase 3: Core Functionality (Week 3)
- [ ] Implement address suggestion tests
- [ ] Implement address validation tests
- [ ] Handle error scenarios

#### Phase 4: User Journeys (Week 4)
- [ ] Implement complete workflow tests
- [ ] Test session management
- [ ] Verify error recovery

#### Phase 5: Visual Testing (Week 5)
- [ ] Implement visual regression tests
- [ ] Responsive design verification
- [ ] Create visual baseline

#### Phase 6: Maintenance (Ongoing)
- [ ] Regular test execution
- [ ] Failure analysis and fixes
- [ ] Test optimization
- [ ] Documentation updates

### How to Use This Documentation

1. **For Test Planning**: Read TEST_PLAN.md first
2. **For Test Strategy**: Read TEST_STRATEGY.md for overall approach
3. **For Test Design**: Read TEST_SCENARIOS.md for test flow
4. **For Implementation**: Use DETAILED_TEST_CASES.md as specification
5. **For Quick Reference**: Use this guide

### Test Execution

#### Local Development
```bash
# Install Playwright
pip install playwright

# Install browser binaries
playwright install

# Run all tests with browser visible
pytest tests/ -v --headed

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_valid_login -v

# Run with video recording
pytest tests/ -v --video=on
```

#### CI/CD Execution
- Tests run automatically on push to `practice` and `main` branches
- Results published to GitHub Pages
- Screenshots/videos attached on failure

### Test Data Requirements

#### Cognito Test Account
- Email: [Your test email]
- Password: [Your test password]
- User Pool ID: ap-southeast-2_2oQQDAKa4
- Client ID: 4p7i1nq2t426jufkh0pe7fgo2u
- Region: ap-southeast-2

#### Test Addresses
- Valid NZ Address: "1 Queen Street, Auckland, 1010"
- Invalid Address: "999 Fake Street, Nowhere"
- Partial Address for Suggestions: "123 Main"

### Success Criteria

- **Test Pass Rate**: ≥ 95%
- **Test Execution Time**: < 5 minutes total
- **Coverage**: All critical user workflows
- **Documentation**: Complete and accurate

### Key Test Scenarios

1. **Authentication Flow**
   - User logs in with valid credentials
   - User logs out successfully
   - Protected endpoints reject invalid tokens
   - Token expiration handled gracefully

2. **Address Validation Flow**
   - User enters partial address
   - Suggestions appear
   - User selects suggestion
   - User validates address
   - Result displayed correctly

3. **Error Scenarios**
   - Network errors handled
   - API timeouts handled
   - Invalid data handled
   - User informed of errors

### Reporting

Test results are reported via:
1. **HTML Reports**: Generated by pytest-html
2. **Custom Dashboard**: Shows test trends
3. **Screenshots**: Captured on failure
4. **Videos**: Recorded on failure (CI/CD)
5. **GitHub Actions**: Integration with CI/CD pipeline

### Browser Support

- Chromium (primary)
- Firefox (optional)
- Safari (optional via webkit)
- Mobile emulation (responsive testing)

### Performance Baselines

- Login flow: 3-5 seconds
- Address suggestions: 1-3 seconds
- Address validation: 3-5 seconds
- Full workflow: < 30 seconds

### Maintenance Schedule

- **Daily**: Check test results
- **Weekly**: Review flaky tests, optimize timeouts
- **Monthly**: Update test data, review coverage
- **Quarterly**: Strategy review, update test plan

### Next Steps

1. Review all documentation files
2. Understand test scenarios and cases
3. Prepare test environment:
   - Install Playwright
   - Create test user in Cognito
   - Prepare test data
4. Start implementing tests based on DETAILED_TEST_CASES.md
5. Set up CI/CD integration
6. Create reporting dashboard

### Questions?

Refer to:
- TEST_STRATEGY.md - For strategic questions
- TEST_PLAN.md - For planning and scheduling
- TEST_SCENARIOS.md - For test flows
- DETAILED_TEST_CASES.md - For test specifications

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19  
**Framework**: Playwright (Python)  
**Status**: Ready for Implementation
