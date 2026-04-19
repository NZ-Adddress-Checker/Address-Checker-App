# Playwright Automation Guide - POM Model

## Overview

Automated tests using **Playwright** with **Page Object Model (POM)** architecture. Currently includes:
- **3 Smoke Tests** - Basic functionality verification
- **5 Sanity Tests** - Key features verification

## Project Structure

```
tests/
├── conftest.py                  # Pytest fixtures and configuration
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
│
├── pages/                       # Page Object Models
│   ├── __init__.py
│   ├── base_page.py            # Base class for all pages
│   ├── login_page.py           # Login page object
│   └── main_page.py            # Main application page object
│
├── utils/                       # Test utilities
│   ├── __init__.py
│   └── test_data.py            # Test data constants
│
├── smoke/                       # Smoke tests
│   ├── __init__.py
│   └── test_smoke.py           # 3 smoke test cases
│
└── sanity/                      # Sanity tests
    ├── __init__.py
    └── test_sanity.py          # 5 sanity test cases
```

## Test Cases

### Smoke Tests (3 tests)

| Test ID | Test Name | Maps To | Purpose |
|---------|-----------|---------|---------|
| SMOKE-001 | Valid Login | TC-AUTH-001 | Verify authentication works |
| SMOKE-002 | Address Suggestions | TC-ADDR-001 | Verify autocomplete API |
| SMOKE-003 | Valid Address Validation | TC-VAL-001 | Verify validation API |

### Sanity Tests (5 tests)

| Test ID | Test Name | Maps To | Purpose |
|---------|-----------|---------|---------|
| SANITY-001 | Invalid Login | TC-AUTH-002 | Verify invalid credentials rejected |
| SANITY-002 | Logout | TC-AUTH-003 | Verify logout clears session |
| SANITY-003 | Select Suggestion | TC-ADDR-003 | Verify suggestion selection |
| SANITY-004 | Invalid Address | TC-VAL-002 | Verify invalid address rejected |
| SANITY-005 | Complete Workflow | TC-JRN-001 | Verify end-to-end flow |

## Page Object Model (POM)

### Base Page Class
All pages inherit from `BasePage` with common methods:
- `navigate()` - Navigate to page
- `click_element()` - Click element
- `fill_input()` - Fill input field
- `wait_for_element()` - Wait for element
- `is_element_visible()` - Check visibility
- `take_screenshot()` - Capture screenshot

### Login Page Object
Methods:
- `navigate()` - Go to login page
- `enter_email()` - Enter email
- `enter_password()` - Enter password
- `click_sign_in()` - Click sign in button
- `login()` - Complete login flow
- `is_login_page_visible()` - Check login page visible
- `is_error_message_visible()` - Check error message
- `get_error_message()` - Get error text

### Main Page Object
Methods:
- `is_authenticated()` - Check if user logged in
- `sign_out()` - Logout user
- `enter_address()` - Enter address in field
- `click_validate()` - Click validate button
- `wait_for_suggestions()` - Wait for suggestions dropdown
- `get_suggestions()` - Get list of suggestions
- `select_first_suggestion()` - Select first suggestion
- `wait_for_validation_result()` - Wait for result
- `get_validation_result()` - Get result text

## Setup & Installation

### 1. Install Dependencies

```bash
# Install Playwright and pytest
pip install playwright pytest python-dotenv

# Install browser binaries
playwright install chromium
```

### 2. Environment Configuration

```bash
# Copy example file
cp tests/.env.example tests/.env

# Edit .env with your values
# - TEST_USER_EMAIL: Cognito test user email
# - TEST_USER_PASSWORD: Cognito test user password
# - BASE_URL: Application URL (default: http://localhost:8080)
# - HEADLESS: Run headless (default: false - show browser)
```

### 3. Start Application

```bash
# Terminal 1: Start Docker containers
docker-compose up

# Wait for services to start:
# - Frontend: http://localhost:8080
# - Backend: http://localhost:8000
```

## Running Tests

### Run All Smoke & Sanity Tests

```bash
# Run all tests
pytest tests/smoke tests/sanity -v

# Run with browser visible (default)
pytest tests/smoke tests/sanity -v

# Run headless
HEADLESS=true pytest tests/smoke tests/sanity -v
```

### Run Smoke Tests Only

```bash
pytest tests/smoke -v
```

### Run Sanity Tests Only

```bash
pytest tests/sanity -v
```

### Run Single Test

```bash
# Run specific test file
pytest tests/smoke/test_smoke.py -v

# Run specific test case
pytest tests/smoke/test_smoke.py::TestSmokeLogin::test_smoke_valid_login -v
```

### Run with Options

```bash
# Verbose output with detailed failures
pytest tests/smoke tests/sanity -vv --tb=long

# Show print statements
pytest tests/smoke tests/sanity -v -s

# Run with specific timeout
TIMEOUT=60000 pytest tests/smoke tests/sanity -v

# Run with slow motion (100ms between actions)
SLOW_MO=100 pytest tests/smoke tests/sanity -v
```

## Test Configuration

### Fixtures (conftest.py)

```python
# Session-scoped browser (reused across tests)
browser

# Function-scoped context (new per test)
context

# Function-scoped page (new per test)
page

# Authenticated page (user logged in)
authenticated_page

# Unauthenticated page (cleared localStorage)
unauthenticated_page
```

### Environment Variables

```bash
# URLs
BASE_URL=http://localhost:8080
BACKEND_URL=http://localhost:8000

# Credentials
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=TestPass123!

# Browser
HEADLESS=false           # Show browser (true for CI/CD)
SLOW_MO=0               # Delay between actions (ms)
TIMEOUT=30000           # Default timeout (ms)

# Test Data
VALID_ADDRESS=...
PARTIAL_ADDRESS=...
INVALID_ADDRESS=...
```

## Test Results

### Console Output

```
tests/smoke/test_smoke.py::TestSmokeLogin::test_smoke_valid_login PASSED
tests/smoke/test_smoke.py::TestSmokeAddressSuggestions::test_smoke_address_suggestions PASSED
tests/smoke/test_smoke.py::TestSmokeAddressValidation::test_smoke_valid_address_validation PASSED

tests/sanity/test_sanity.py::TestSanityAuthentication::test_sanity_invalid_login PASSED
tests/sanity/test_sanity.py::TestSanityAuthentication::test_sanity_logout PASSED
tests/sanity/test_sanity.py::TestSanityAddressFeatures::test_sanity_select_suggestion PASSED
tests/sanity/test_sanity.py::TestSanityAddressFeatures::test_sanity_invalid_address_validation PASSED
tests/sanity/test_sanity.py::TestSanityEndToEndWorkflow::test_sanity_complete_address_workflow PASSED

====================== 8 passed in 45.32s ======================
```

### Test Execution Flow

Each test:
1. **Setup** - Create browser context and page
2. **Arrange** - Set up test data and page objects
3. **Act** - Perform user actions
4. **Assert** - Verify expected outcomes
5. **Cleanup** - Close page and context

## Best Practices

### 1. Use Page Objects
- Create page objects for each page
- Encapsulate selectors in page objects
- Reuse methods across tests

### 2. Wait for Elements
```python
# Good - wait for element explicitly
main_page.wait_for_suggestions(timeout=5000)

# Avoid - hardcoded waits
page.wait_for_timeout(1000)
```

### 3. Use Fixtures
```python
# Good - use fixture
def test_example(authenticated_page):
    main_page = MainPage(authenticated_page)

# Avoid - manual setup
def test_example(page):
    # manual login code
```

### 4. Clear Assertions
```python
# Good - specific assertion
assert "valid" in result.lower(), f"Expected valid result, got: {result}"

# Avoid - vague assertion
assert result
```

### 5. Test Independence
- Each test should be independent
- Use fixtures for setup/teardown
- Clear state between tests

## Debugging

### Run Test with Debug Output

```bash
# Show all print statements
pytest tests/smoke/test_smoke.py::TestSmokeLogin::test_smoke_valid_login -v -s

# Pause on failure
pytest tests/smoke/test_smoke.py -v --pdb
```

### Take Screenshots

```python
# In test code
page.screenshot(path="screenshot.png")

# Or in fixture
@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    if request.node.rep_call.failed:
        page.screenshot(path=f"failure-{request.node.name}.png")
```

### View Page State

```python
# Print page title
print(page.title())

# Print current URL
print(page.url)

# Print page HTML
print(page.content())
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run Smoke & Sanity Tests
  run: |
    HEADLESS=true pytest tests/smoke tests/sanity -v --tb=short
```

### Environment Setup for CI/CD

```bash
# In CI/CD pipeline, set:
- HEADLESS=true         # Run headless
- BASE_URL=http://host  # Test environment URL
- TIMEOUT=60000         # Longer timeout for CI
```

## Troubleshooting

### Common Issues

**Issue**: Tests timeout on selectors
- **Solution**: Increase TIMEOUT in .env or use explicit waits

**Issue**: Login fails
- **Solution**: Verify TEST_USER_EMAIL and TEST_USER_PASSWORD in .env

**Issue**: Suggestions don't appear
- **Solution**: Check PARTIAL_ADDRESS in .env matches data in NZ Post

**Issue**: API returns 401
- **Solution**: Verify Cognito credentials and JWT configuration in backend

### Debug Checklist

- [ ] Application running (`docker-compose ps`)
- [ ] .env file exists with correct credentials
- [ ] Browser visible (HEADLESS=false)
- [ ] Print test output (use -s flag)
- [ ] Take screenshots on failure
- [ ] Check browser developer tools (F12)

## Next Steps

1. **Verify Setup**: Run smoke tests successfully
2. **Implement P0/P1 Tests**: Add critical test gaps
3. **Set up Reporting**: Generate HTML reports
4. **Configure CI/CD**: Add to GitHub Actions
5. **Scale Tests**: Add remaining test cases

## References

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://martinfowler.com/bliki/PageObject.html)

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19  
**Framework**: Playwright (Python) with POM
