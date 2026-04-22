# Test Strategy - NZ Address Checker

## 🎯 Testing Objectives

The automation test suite aims to ensure the NZ Address Checker application:
1. ✅ Authenticates users securely via AWS Cognito
2. ✅ Enforces role-based access control (AddressValidators group)
3. ✅ Provides accurate address autocomplete functionality
4. ✅ Validates addresses against NZ Post data
5. ✅ Handles errors gracefully (API failures, rate limits, network issues)
6. ✅ Maintains security against common vulnerabilities

## 📊 Test Pyramid

```
         /\
        /UI\          4 tests - Critical user flows
       /----\
      / API  \        9 tests - Business logic, auth, validation
     /--------\
    / Security \      3 tests - JWT, token tampering, auth bypass
   /------------\
```

### Layer Distribution
- **UI Tests (25%)**: End-to-end user journeys, critical workflows
- **API Tests (55%)**: Authentication, authorization, data validation
- **Security Tests (20%)**: Vulnerability testing, token validation

## 🧪 Test Scope

### In Scope

#### ✅ Functional Testing
- User authentication (login/logout)
- Address autocomplete search
- Dropdown suggestion display
- Address validation workflow
- Access control enforcement

#### ✅ Security Testing
- JWT token validation
- Token tampering detection
- Authentication bypass prevention
- Authorization checks
- Group-based access control

#### ✅ Integration Testing
- Frontend-Backend communication
- Backend-External API integration
- AWS Cognito authentication flow
- Addressable API contract validation

#### ✅ Error Handling
- API unavailability scenarios
- Rate limiting responses
- Network timeout handling
- Invalid input validation
- Missing authentication headers

### Out of Scope

#### ❌ Not Covered
- Performance/load testing (future enhancement)
- Cross-browser testing (Chrome only currently)
- Mobile responsive testing
- Accessibility testing (WCAG compliance)
- Database testing (no direct DB access)
- Infrastructure/deployment testing

## 🎨 Test Design Patterns

### 1. Page Object Model (POM)
**Purpose**: Separate page structure from test logic

**Implementation**:
```python
# pages/login_page.py
class LoginPage(BasePage):
    START = "text=Start"
    USERNAME = "input[name='username']"
    
    def login(self, user, pwd):
        # Encapsulates login flow
        self.click(self.START)
        self.fill(self.USERNAME, user)
        # ...
```

**Benefits**:
- ✅ Reusability across tests
- ✅ Easy maintenance when UI changes
- ✅ Reduced code duplication
- ✅ Clear separation of concerns

### 2. Test Isolation
**Purpose**: Each test runs independently

**Implementation**:
- Fresh browser context per test (`conftest.py`)
- LocalStorage cleanup between tests
- No shared state between tests
- Independent test data

### 3. Explicit Waits
**Purpose**: Handle dynamic page loading

**Strategies**:
- `wait_until="networkidle"` for initial page loads
- `expect().to_be_visible()` for dynamic elements
- Retry logic for flaky interactions
- Timeout configurations per action

### 4. Conditional Testing
**Purpose**: Handle variable external dependencies

**Example**:
```python
# Handle both success and API error scenarios
if dashboard.has_error():
    error_msg = dashboard.get_error_message()
    assert "temporarily unavailable" in error_msg or "rate limit" in error_msg
else:
    # Normal flow validation
    assert dashboard.has_dropdown()
```

## 🔍 Test Categories

### 1. Smoke Tests
**Frequency**: Every commit  
**Duration**: ~15 seconds  
**Tests**: Basic login, API health

### 2. Regression Tests
**Frequency**: Before release  
**Duration**: ~45 seconds  
**Tests**: Full suite (all tests)

### 3. External API Tests
**Frequency**: On-demand only  
**Duration**: ~5 seconds  
**Tests**: Addressable API contract tests  
**Note**: Skipped by default (rate limit preservation)

## 📋 Test Data Strategy

### Static Test Data
- **Location**: `config.py`
- **Type**: User credentials, URLs, API keys
- **Maintenance**: Manual updates as needed

### Dynamic Test Data
- **Source**: API responses, real-time data
- **Validation**: Schema validation via `schemas/`
- **Cleanup**: Not applicable (read-only operations)

### Test Users

| User | Purpose | Access Level | Expected Result |
|------|---------|--------------|-----------------|
| testapp | Valid user | AddressValidators | Full access |
| jeffcj | Invalid user | None | Access denied |

## 🎯 Test Execution Strategy

### Local Development
```bash
# Quick smoke test
pytest Tests/test_ui_flow.py::test_valid_user_flow -v

# Full regression
pytest -v
```

### CI/CD Pipeline (Future)
```yaml
# Planned: GitHub Actions workflow
stages:
  - smoke_tests (on PR)
  - regression_tests (on merge)
  - nightly_full_suite (includes external)
```

## 📊 Success Criteria

### Test Execution
- ✅ 100% pass rate for core tests
- ✅ External API tests: Optional (rate limit dependent)
- ✅ Execution time: < 60 seconds
- ✅ No false positives/negatives

### Test Reliability
- ✅ Retry logic for known flaky scenarios
- ✅ Clear failure messages
- ✅ Consistent results across runs
- ✅ Test isolation verified

### Coverage Goals
- ✅ Critical user paths: 100%
- ✅ API endpoints: 100%
- ✅ Security scenarios: 80%+
- ✅ Error scenarios: 70%+

## 🚨 Defect Management

### Bug Reporting Template
```
Title: [Component] Brief description
Severity: Critical/High/Medium/Low
Steps to Reproduce:
1. ...
2. ...
Expected: ...
Actual: ...
Test: test_name.py::test_function
```

### Severity Levels
- **Critical**: Security breach, data loss, complete failure
- **High**: Major feature broken, no workaround
- **Medium**: Feature partially broken, workaround exists
- **Low**: Cosmetic, minor inconvenience

## 🔄 Test Maintenance

### When to Update Tests

#### UI Changes
- Update page object selectors in `pages/`
- Verify wait strategies still appropriate
- Update test data if UI validation changes

#### API Changes
- Update schemas in `schemas/`
- Modify endpoint tests in `Tests/test_*_api.py`
- Update authentication logic if auth flow changes

#### New Features
- Add new page objects if new pages introduced
- Create new test file following naming convention
- Update `config.py` with new test data

### Review Cycle
- **Weekly**: Review test failures and flakiness
- **Monthly**: Update documentation, dependencies
- **Quarterly**: Assess test coverage, add missing scenarios

## 🎓 Best Practices

### Test Writing
1. ✅ **One assertion per concept** (multiple asserts OK if testing same thing)
2. ✅ **Descriptive test names** (`test_invalid_user_cannot_access_dashboard`)
3. ✅ **Arrange-Act-Assert** pattern
4. ✅ **Test independence** (no test depends on another)
5. ✅ **Assertion messages** (`assert value, "Expected X but got Y"`)

### Code Quality
1. ✅ **DRY principle** (Don't Repeat Yourself)
2. ✅ **Clear variable names** (`dropdown_visible` not `d_v`)
3. ✅ **Comments for complex logic** only
4. ✅ **Consistent formatting** (follow PEP 8)
5. ✅ **Type hints** where beneficial

### Performance
1. ✅ **Minimize page loads** (test multiple things per session)
2. ✅ **Skip unnecessary waits** (use explicit waits, not time.sleep)
3. ✅ **Parallel execution** (future: pytest-xdist)
4. ✅ **Targeted test runs** (don't run full suite for small changes)

## 📈 Future Enhancements

### Planned Improvements
1. 🔮 **CI/CD Integration** (GitHub Actions)
2. 🔮 **Parallel Execution** (pytest-xdist)
3. 🔮 **Visual Regression** (screenshot comparison)
4. 🔮 **Performance Testing** (response time assertions)
5. 🔮 **Cross-browser Testing** (Firefox, Safari)
6. 🔮 **Mobile Testing** (responsive layouts)
7. 🔮 **Accessibility Testing** (WCAG compliance)
8. 🔮 **Test Data Factories** (dynamic test data generation)

### Technical Debt
- Add structured logging (currently print statements)
- Environment variable management for secrets
- Database state verification (if DB access granted)
- API mocking for external dependencies (Addressable API)

## 📞 Ownership & Responsibilities

### Test Maintenance
- Update tests when features change
- Fix failing tests within 24 hours
- Review and approve test PRs

### Test Execution
- Run smoke tests before commits
- Run full suite before deployments
- Monitor test execution times

### Test Reporting
- Review HTML reports after each run
- Log defects for failing tests
- Track test coverage metrics
