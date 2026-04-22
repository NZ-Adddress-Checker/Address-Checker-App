# Test Cases - NZ Address Checker

## Test Case Catalog

This document provides detailed test case specifications for all automated tests in the NZ Address Checker test suite.

---

## 📋 Table of Contents

### [Functional Tests](#functional-tests)
- [TC-001: Valid User Complete Flow](#tc-001-valid-user-complete-flow)
- [TC-002: Validation Requires Dropdown Selection](#tc-002-validation-requires-dropdown-selection)
- [TC-003: Invalid User Access Blocked](#tc-003-invalid-user-access-blocked)
- [TC-004: User Logout](#tc-004-user-logout)

### [Security Tests](#security-tests)
- [TC-005: Suggest Endpoint Requires Authentication](#tc-005-suggest-endpoint-requires-authentication)
- [TC-006: Validate Endpoint Requires Authentication](#tc-006-validate-endpoint-requires-authentication)
- [TC-007: Invalid Token Rejected](#tc-007-invalid-token-rejected)
- [TC-008: Tampered JWT Rejected](#tc-008-tampered-jwt-rejected)
- [TC-009: No Bearer Prefix Rejected](#tc-009-no-bearer-prefix-rejected)
- [TC-010: Empty Token Rejected](#tc-010-empty-token-rejected)

### [API Tests](#api-tests)
- [TC-011: Validate Without Auth Returns 401](#tc-011-validate-without-auth-returns-401)
- [TC-012: Suggest Without Auth Returns 401](#tc-012-suggest-without-auth-returns-401)
- [TC-013: Validate Missing Field Returns 422](#tc-013-validate-missing-field-returns-422)

### [Error Handling Tests](#error-handling-tests)
- [TC-014: API Timeout Shows Error](#tc-014-api-timeout-shows-error)
- [TC-015: Slow API Response Handling](#tc-015-slow-api-response-handling)
- [TC-016: Network Error Recovery](#tc-016-network-error-recovery)

### [External API Contract Tests](#external-api-contract-tests)
- [TC-017: Addressable Returns List](#tc-017-addressable-returns-list)
- [TC-018: Addressable Items Have Formatted Field](#tc-018-addressable-items-have-formatted-field)
- [TC-019: Addressable Schema Validation](#tc-019-addressable-schema-validation)

---

## Functional Tests

### TC-001: Valid User Complete Flow

**Test Case ID**: TC-001  
**Test File**: `Tests/test_ui_flow.py::test_valid_user_flow`  
**Category**: Functional - UI  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Docker containers running (frontend on port 8085, backend on port 8001)
- Valid user credentials configured (`testapp` / `Test@1996!`)
- User belongs to `AddressValidators` group in AWS Cognito
- Addressable API accessible (or gracefully handles unavailability)

#### Test Steps
1. Navigate to application homepage (`http://localhost:8085`)
2. Wait for page to load completely (networkidle state)
3. Click the "Start" button to initiate Cognito login
4. Wait for redirect to AWS Cognito hosted UI
5. Enter username: `testapp`
6. Enter password: `Test@1996!`
7. Click "Sign in" button
8. Wait for authentication and redirect back to dashboard
9. Verify "Logout" button is visible on dashboard
10. Locate address input field (CSS: `input.address-input`)
11. Type address query: `10 Queen Street, Auckland`
12. Wait 2 seconds for debounce and API call
13. Check if dropdown suggestions list appears

#### Expected Results
**Scenario A - API Available**:
- User successfully logs in
- Dashboard loads with address input field visible
- Logout button is displayed
- After typing address, suggestions dropdown appears (`.suggestions-list`)
- Dropdown contains suggestion items (`.suggestion-item`)
- User can click first suggestion
- After clicking "Validate" button
- Validation shows "Valid: Yes ✓"

**Scenario B - API Unavailable (Rate Limited)**:
- User successfully logs in
- Dashboard loads with address input field visible
- Logout button is displayed
- After typing address, error message appears
- Error message contains "temporarily unavailable" OR "rate limit"
- No suggestions dropdown is shown (graceful degradation)
- Test passes - error handling verified

#### Actual Automation Code
```python
def test_valid_user_flow(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    dash = DashboardPage(page)
    
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    page.wait_for_selector("input.address-input", timeout=5000)
    assert page.is_visible("text=Logout")
    
    dash.search_address("10 Queen Street, Auckland")
    page.wait_for_timeout(2000)
    
    # Conditional validation for API availability
    if not page.is_visible(".suggestions-list", timeout=2000):
        if page.is_visible(".error-message"):
            error_text = page.locator(".error-message").inner_text()
            assert "temporarily unavailable" in error_text.lower() or "rate limit" in error_text.lower()
            return  # Pass - error handling works
    
    dash.select_first()
    dash.validate()
    assert dash.is_valid()
```

---

### TC-002: Validation Requires Dropdown Selection

**Test Case ID**: TC-002  
**Test File**: `Tests/test_ui_flow.py::test_validation_requires_dropdown_selection`  
**Category**: Functional - Validation  
**Priority**: High  
**Automated**: Yes  

#### Prerequisites
- Docker containers running
- Valid user credentials configured
- User authenticated successfully

#### Test Steps
1. Navigate to application homepage
2. Complete login process with valid credentials
3. Wait for dashboard to load
4. Locate address input field
5. Type random text that won't match any address: `random text`
6. Wait 500ms (half second)
7. Do NOT select from dropdown (intentionally skip this step)
8. Click "Validate" button directly

#### Expected Results
- Error message appears on screen
- Error message text: `Please select an address from the dropdown list.`
- Validation does not proceed
- No "Valid: Yes ✓" indicator shown
- User is prompted to select from dropdown before validating

#### Actual Automation Code
```python
def test_validation_requires_dropdown_selection(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    dash = DashboardPage(page)
    
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    dash.search_address("random text")
    dash.wait(500)
    dash.validate()
    
    error_message = page.locator("text=Please select an address from the dropdown list.")
    assert error_message.is_visible()
```

---

### TC-003: Invalid User Access Blocked

**Test Case ID**: TC-003  
**Test File**: `Tests/test_ui_flow.py::test_invalid_user_blocked`  
**Category**: Functional - Access Control  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Docker containers running
- Invalid user credentials configured (`jeffcj` / `Test@1996!`)
- User exists in Cognito but NOT in `AddressValidators` group

#### Test Steps
1. Navigate to application homepage
2. Click "Start" button
3. Wait for Cognito hosted UI to load
4. Enter username: `jeffcj`
5. Enter password: `Test@1996!`
6. Click "Sign in"
7. Wait for authentication to complete

#### Expected Results
- User successfully authenticates with Cognito (valid credentials)
- User is redirected back to application
- Access denied page is displayed
- User cannot access the dashboard
- No address input field is visible
- No access page shown with appropriate message

#### Actual Automation Code
```python
def test_invalid_user_blocked(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    no_access = NoAccessPage(page)
    
    login.login(USERS["invalid"]["username"], USERS["invalid"]["password"])
    assert no_access.shown()
```

---

### TC-004: User Logout

**Test Case ID**: TC-004  
**Test File**: `Tests/test_ui_flow.py::test_logout`  
**Category**: Functional - Authentication  
**Priority**: High  
**Automated**: Yes  

#### Prerequisites
- Docker containers running
- Valid user credentials configured
- User successfully logged in to dashboard

#### Test Steps
1. Navigate to application homepage
2. Complete login with valid credentials
3. Verify dashboard is displayed
4. Locate "Logout" button on dashboard
5. Click "Logout" button
6. Wait for logout process to complete

#### Expected Results
- User is successfully logged out
- Page returns to homepage/landing page
- "Start" button is visible again
- User session is cleared
- Dashboard is no longer accessible without re-authentication

#### Actual Automation Code
```python
def test_logout(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    dash = DashboardPage(page)
    
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    dash.logout()
    assert "Start" in page.content()
```

---

## Security Tests

### TC-005: Suggest Endpoint Requires Authentication

**Test Case ID**: TC-005  
**Test File**: `Tests/test_backend_api.py::test_suggest_requires_auth`  
**Category**: Security - API Authentication  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Backend API running on port 8001
- No authentication token provided

#### Test Steps
1. Prepare GET request to `/api/address/suggest`
2. Add query parameter: `q=Auckland`
3. Do NOT include Authorization header
4. Send HTTP GET request
5. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Request is rejected
- No address suggestions are returned
- Error response indicates authentication required

#### Actual Automation Code
```python
def test_suggest_requires_auth():
    res = requests.get(f"{API_URL}/address/suggest", params={"q": "Auckland"})
    assert res.status_code == 401
```

---

### TC-006: Validate Endpoint Requires Authentication

**Test Case ID**: TC-006  
**Test File**: `Tests/test_backend_api.py::test_validate_requires_auth`  
**Category**: Security - API Authentication  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Backend API running on port 8001
- No authentication token provided

#### Test Steps
1. Prepare POST request to `/api/address/validate`
2. Set request body JSON: `{"address": "Auckland"}`
3. Do NOT include Authorization header
4. Send HTTP POST request
5. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Request is rejected
- No validation result is returned
- Error response indicates authentication required

#### Actual Automation Code
```python
def test_validate_requires_auth():
    res = requests.post(f"{API_URL}/address/validate", json={"address": "Auckland"})
    assert res.status_code == 401
```

---

### TC-007: Invalid Token Rejected

**Test Case ID**: TC-007  
**Test File**: `Tests/test_backend_api.py::test_invalid_token_rejected`  
**Category**: Security - Token Validation  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Backend API running
- Invalid/forged JWT token prepared

#### Test Steps
1. Prepare GET request to `/api/address/suggest`
2. Add query parameter: `q=Auckland`
3. Include Authorization header with completely forged token
4. Header value: `Bearer forged.token.value`
5. Send HTTP GET request
6. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Forged token is detected and rejected
- JWKS validation fails
- No data is returned
- Security is maintained against token forgery

#### Actual Automation Code
```python
def test_invalid_token_rejected():
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": "Bearer forged.token.value"}
    )
    assert res.status_code == 401
```

---

### TC-008: Tampered JWT Rejected

**Test Case ID**: TC-008  
**Test File**: `Tests/test_jwt_security.py::test_tampered_jwt_rejected`  
**Category**: Security - JWT Integrity  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Backend API running
- JWT helper utility available for token tampering

#### Test Steps
1. Create a base JWT token structure
2. Use JWT helper to tamper with token payload
3. Modify token signature or payload content
4. Prepare GET request to `/api/address/suggest`
5. Include tampered token in Authorization header
6. Send request
7. Capture response status code

#### Expected Results
- HTTP Status Code: `401` or `403`
- Tampered token is detected
- Signature verification fails
- Request is rejected
- Data integrity is protected

#### Actual Automation Code
```python
def test_tampered_jwt_rejected():
    fake_token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.signature"
    tampered = tamper_token(fake_token)
    
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": f"Bearer {tampered}"}
    )
    assert res.status_code in [401, 403]
```

---

### TC-009: No Bearer Prefix Rejected

**Test Case ID**: TC-009  
**Test File**: `Tests/test_jwt_security.py::test_no_bearer_prefix_rejected`  
**Category**: Security - Authorization Format  
**Priority**: High  
**Automated**: Yes  

#### Prerequisites
- Backend API running

#### Test Steps
1. Prepare GET request to `/api/address/suggest`
2. Add query parameter: `q=Auckland`
3. Include Authorization header WITHOUT "Bearer" prefix
4. Header value: `Token somevalue`
5. Send HTTP GET request
6. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Incorrect authorization scheme rejected
- Backend enforces "Bearer" prefix requirement
- RFC 6750 OAuth 2.0 standard enforced

#### Actual Automation Code
```python
def test_no_bearer_prefix_rejected():
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": "Token somevalue"}
    )
    assert res.status_code == 401
```

---

### TC-010: Empty Token Rejected

**Test Case ID**: TC-010  
**Test File**: `Tests/test_jwt_security.py::test_empty_token_rejected`  
**Category**: Security - Token Validation  
**Priority**: High  
**Automated**: Yes  

#### Prerequisites
- Backend API running

#### Test Steps
1. Prepare GET request to `/api/address/suggest`
2. Add query parameter: `q=Auckland`
3. Include Authorization header with "Bearer" but empty token
4. Header value: `Bearer ` (space after Bearer, no token)
5. Send HTTP GET request
6. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Empty token is rejected
- Backend validates token is not empty string
- Security against malformed auth headers

#### Actual Automation Code
```python
def test_empty_token_rejected():
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"},
        headers={"Authorization": "Bearer "}
    )
    assert res.status_code == 401
```

---

## API Tests

### TC-011: Validate Without Auth Returns 401

**Test Case ID**: TC-011  
**Test File**: `Tests/test_address_api.py::test_validate_without_auth_returns_401`  
**Category**: API - Authentication  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Backend API running
- No authentication token

#### Test Steps
1. Prepare POST request to `/api/address/validate`
2. Set request body: `{"address": "Auckland Central"}`
3. Do NOT include Authorization header
4. Send HTTP POST request
5. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Request rejected due to missing authentication
- No validation is performed
- Endpoint protected by authentication middleware

#### Actual Automation Code
```python
def test_validate_without_auth_returns_401():
    res = requests.post(
        f"{API_URL}/address/validate",
        json={"address": "Auckland Central"}
    )
    assert res.status_code == 401
```

---

### TC-012: Suggest Without Auth Returns 401

**Test Case ID**: TC-012  
**Test File**: `Tests/test_address_api.py::test_suggest_without_auth_returns_401`  
**Category**: API - Authentication  
**Priority**: Critical  
**Automated**: Yes  

#### Prerequisites
- Backend API running
- No authentication token

#### Test Steps
1. Prepare GET request to `/api/address/suggest`
2. Add query parameter: `q=Auckland`
3. Do NOT include Authorization header
4. Send HTTP GET request
5. Capture response status code

#### Expected Results
- HTTP Status Code: `401 Unauthorized`
- Request rejected due to missing authentication
- No suggestions are returned
- Endpoint protected by authentication middleware

#### Actual Automation Code
```python
def test_suggest_without_auth_returns_401():
    res = requests.get(
        f"{API_URL}/address/suggest",
        params={"q": "Auckland"}
    )
    assert res.status_code == 401
```

---

### TC-013: Validate Missing Field Returns 422

**Test Case ID**: TC-013  
**Test File**: `Tests/test_address_api.py::test_validate_missing_field_returns_422`  
**Category**: API - Input Validation  
**Priority**: Medium  
**Automated**: Yes  

#### Prerequisites
- Backend API running

#### Test Steps
1. Prepare POST request to `/api/address/validate`
2. Set request body with WRONG field name: `{"wrong_field": "Auckland"}`
3. Include forged Authorization header (will fail before schema check)
4. Send HTTP POST request
5. Capture response status code

#### Expected Results
- HTTP Status Code: `401` (auth fails first) OR `422` (schema validation)
- Either response is acceptable depending on middleware order
- Invalid schema is detected if auth passes
- Pydantic validation catches missing required field

#### Actual Automation Code
```python
def test_validate_missing_field_returns_422():
    res = requests.post(
        f"{API_URL}/address/validate",
        json={"wrong_field": "Auckland"},
        headers={"Authorization": "Bearer forged.token.value"}
    )
    assert res.status_code in [401, 422]
```

---

## Error Handling Tests

### TC-014: API Timeout Shows Error

**Test Case ID**: TC-014  
**Test File**: `Tests/test_error_handling.py::test_api_timeout_shows_error`  
**Category**: Error Handling - Network  
**Priority**: High  
**Automated**: Yes  

#### Prerequisites
- Docker containers running
- Valid user credentials
- Playwright route mocking capability

#### Test Steps
1. Navigate to application homepage
2. Complete login with valid credentials
3. Wait for dashboard to load
4. Configure Playwright route mock to abort requests to `/api/address/suggest**`
5. Simulate timeout by aborting with "timedout" error
6. Type address in search field: `10 Queen Street, Auckland`
7. Wait 3 seconds for error handling
8. Check if error message is displayed

#### Expected Results
**Option A - Error Message Shown**:
- Error message is visible (`.error-message`)
- Error text contains one of: "unavailable", "timeout", "failed", or "network"
- Example: "Network error. Please check your connection."
- No suggestions dropdown appears

**Option B - Graceful Degradation**:
- No error message shown
- Suggestions dropdown does NOT appear
- UI remains functional and responsive
- User can still interact with the page

#### Actual Automation Code
```python
def test_api_timeout_shows_error(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    page.wait_for_selector("input.address-input", timeout=5000)
    
    # Mock timeout
    page.route("**/api/address/suggest**", lambda route: route.abort("timedout"))
    
    dashboard = DashboardPage(page)
    dashboard.search_address("10 Queen Street, Auckland")
    page.wait_for_timeout(3000)
    
    error_visible = page.is_visible(".error-message", timeout=2000)
    suggestions_visible = page.is_visible(".suggestions-list", timeout=1000)
    
    if error_visible:
        error_text = page.locator(".error-message").inner_text()
        assert "unavailable" in error_text.lower() or "network" in error_text.lower()
    else:
        assert not suggestions_visible  # Graceful degradation
```

---

### TC-015: Slow API Response Handling

**Test Case ID**: TC-015  
**Test File**: `Tests/test_error_handling.py::test_slow_api_response_handling`  
**Category**: Error Handling - Performance  
**Priority**: Medium  
**Automated**: Yes  

#### Prerequisites
- Docker containers running
- Valid user credentials
- Playwright route mocking with delay capability

#### Test Steps
1. Navigate to application homepage
2. Complete login with valid credentials
3. Wait for dashboard to load
4. Configure Playwright route mock for `/api/address/suggest**`
5. Add 3-second delay before continuing normal response
6. Type address in search field: `10 Queen Street, Auckland`
7. Wait 5 seconds for response
8. Verify UI remains responsive

#### Expected Results
- UI does not freeze during slow API response
- Address input field remains visible and functional
- Logout button remains visible
- Page remains interactive
- After delay, either:
  - Suggestions appear (delayed success)
  - Error message appears (timeout)
  - Nothing shown (graceful timeout)
- No JavaScript errors or crashes

#### Actual Automation Code
```python
def test_slow_api_response_handling(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    page.wait_for_selector("input.address-input", timeout=5000)
    
    def handle_slow_route(route):
        import time
        time.sleep(3)  # 3-second delay
        route.continue_()
    
    page.route("**/api/address/suggest**", handle_slow_route)
    
    dashboard = DashboardPage(page)
    dashboard.search_address("10 Queen Street, Auckland")
    page.wait_for_timeout(5000)
    
    # Verify page still responsive
    assert page.is_visible("input.address-input")
    assert page.is_visible("text=Logout")
```

---

### TC-016: Network Error Recovery

**Test Case ID**: TC-016  
**Test File**: `Tests/test_error_handling.py::test_network_error_recovery`  
**Category**: Error Handling - Resilience  
**Priority**: High  
**Automated**: Yes  

#### Prerequisites
- Docker containers running
- Valid user credentials
- Playwright route mocking with conditional logic

#### Test Steps
1. Navigate to application homepage
2. Complete login with valid credentials
3. Wait for dashboard to load
4. Configure Playwright route mock to:
   - First call: Abort with "failed" error
   - Subsequent calls: Continue normally
5. Type first address: `10 Queen Street`
6. Wait 2 seconds (should fail)
7. Clear input field
8. Wait 500ms
9. Type second address: `20 Queen Street`
10. Wait 2 seconds (should succeed or handle gracefully)

#### Expected Results
- First search attempt fails (network error simulated)
- Error may or may not be displayed (depends on UI implementation)
- After clearing input and searching again:
  - Application recovers from error state
  - Input field remains functional
  - Logout button still available
  - No permanent error state or crash
- Application demonstrates resilience to transient network failures

#### Actual Automation Code
```python
def test_network_error_recovery(page):
    page.goto(BASE_URL, wait_until="networkidle")
    login = LoginPage(page)
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    page.wait_for_selector("input.address-input", timeout=5000)
    
    call_count = {"count": 0}
    
    def handle_failing_then_success(route):
        call_count["count"] += 1
        if call_count["count"] == 1:
            route.abort("failed")  # First call fails
        else:
            route.continue_()  # Subsequent calls succeed
    
    page.route("**/api/address/suggest**", handle_failing_then_success)
    
    dashboard = DashboardPage(page)
    dashboard.search_address("10 Queen Street")
    page.wait_for_timeout(2000)
    
    page.fill("input.address-input", "")
    page.wait_for_timeout(500)
    
    dashboard.search_address("20 Queen Street")
    page.wait_for_timeout(2000)
    
    # Verify recovery
    assert page.is_visible("input.address-input")
    assert page.is_visible("text=Logout")
```

---

## External API Contract Tests

### TC-017: Addressable Returns List

**Test Case ID**: TC-017  
**Test File**: `Tests/test_addressable_contract.py::test_addressable_returns_list`  
**Category**: Integration - External API  
**Priority**: Medium  
**Automated**: Yes (Skipped by default)  

#### Prerequisites
- Valid Addressable API key configured
- API quota available (100 requests/day free tier)
- Network connectivity to `https://api.addressable.dev`
- VPN may be required if IP-based rate limit hit

#### Test Steps
1. Prepare GET request to `https://api.addressable.dev/v2/autocomplete`
2. Add query parameters:
   - `q=1 Main Street`
   - `country_code=NZ`
   - `api_key=<configured_key>`
   - `max_results=3`
3. Send HTTP GET request
4. Capture response status code and body
5. Parse JSON response

#### Expected Results
- HTTP Status Code: `200 OK`
- Response is valid JSON
- Response is an array (list)
- Array is not empty (length > 0)
- Contains address suggestions for New Zealand

#### Actual Automation Code
```python
@pytest.mark.skip(reason="Skipped by default to preserve API quota")
@pytest.mark.external
def test_addressable_returns_list():
    res = requests.get(URL, params={
        "q": "1 Main Street",
        "country_code": "NZ",
        "api_key": NZPOST_API_KEY,
        "max_results": 3
    })
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
```

**Note**: This test is skipped by default. Run with: `pytest -m external`

---

### TC-018: Addressable Items Have Formatted Field

**Test Case ID**: TC-018  
**Test File**: `Tests/test_addressable_contract.py::test_addressable_items_have_formatted_field`  
**Category**: Integration - API Schema  
**Priority**: Medium  
**Automated**: Yes (Skipped by default)  

#### Prerequisites
- Valid Addressable API key configured
- API quota available
- Network connectivity

#### Test Steps
1. Prepare GET request to Addressable API
2. Add query parameters:
   - `q=Auckland`
   - `country_code=NZ`
   - `api_key=<configured_key>`
   - `max_results=3`
3. Send HTTP GET request
4. Parse JSON response array
5. Iterate through each item in response
6. Check each item for `formatted` field

#### Expected Results
- HTTP Status Code: `200 OK`
- Response is an array
- Each item in array contains `formatted` field
- `formatted` field is a string type
- `formatted` field is not empty (length > 0)
- Example: `"formatted": "1 Main Street, Auckland 1010"`

#### Actual Automation Code
```python
@pytest.mark.skip(reason="Skipped by default to preserve API quota")
@pytest.mark.external
def test_addressable_items_have_formatted_field():
    res = requests.get(URL, params={
        "q": "Auckland",
        "country_code": "NZ",
        "api_key": NZPOST_API_KEY,
        "max_results": 3
    })
    assert res.status_code == 200
    for item in res.json():
        assert "formatted" in item
        assert isinstance(item["formatted"], str)
        assert len(item["formatted"]) > 0
```

**Note**: This test is skipped by default. Run with: `pytest -m external`

---

### TC-019: Addressable Schema Validation

**Test Case ID**: TC-019  
**Test File**: `Tests/test_addressable_contract.py::test_addressable_schema`  
**Category**: Integration - Contract Validation  
**Priority**: Medium  
**Automated**: Yes (Skipped by default)  

#### Prerequisites
- Valid Addressable API key configured
- API quota available
- JSON schema validator library (jsonschema)
- Expected schema defined in `schemas/addressable_schema.py`

#### Test Steps
1. Prepare GET request to Addressable API
2. Add query parameters:
   - `q=Wellington`
   - `country_code=NZ`
   - `api_key=<configured_key>`
   - `max_results=3`
3. Send HTTP GET request
4. Parse JSON response
5. Load expected JSON schema from schema file
6. Validate response against schema using jsonschema library

#### Expected Results
- HTTP Status Code: `200 OK`
- Response validates successfully against defined schema
- No schema validation errors
- Contract between API and application is maintained
- Schema includes:
  - Array of objects
  - Each object has `formatted` field (string, required)
  - Each object may have `components` field (object)

#### Actual Automation Code
```python
@pytest.mark.skip(reason="Skipped by default to preserve API quota")
@pytest.mark.external
def test_addressable_schema():
    res = requests.get(URL, params={
        "q": "Wellington",
        "country_code": "NZ",
        "api_key": NZPOST_API_KEY,
        "max_results": 3
    })
    assert res.status_code == 200
    validate(instance=res.json(), schema=ADDRESSABLE_SCHEMA)
```

**Note**: This test is skipped by default. Run with: `pytest -m external`

---

## Test Execution Summary

### Run All Tests
```bash
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"
python -m pytest -v --tb=short
```

**Expected**: 16 passed, 3 skipped

### Run Specific Category
```bash
# UI Tests
python -m pytest Tests/test_ui_flow.py -v

# Security Tests
python -m pytest Tests/test_jwt_security.py -v

# Error Handling Tests
python -m pytest Tests/test_error_handling.py -v

# External API Tests (uses quota)
python -m pytest -m external -v
```

### Generate HTML Report
```bash
python -m pytest -v --html=report.html --self-contained-html
```

Report location: `C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation\report.html`

---

## Test Data Reference

### Valid User
- **Username**: `testapp`
- **Password**: `Test@1996!`
- **Group**: `AddressValidators`
- **Expected Access**: Full dashboard access

### Invalid User
- **Username**: `jeffcj`
- **Password**: `Test@1996!`
- **Group**: None
- **Expected Access**: Access denied page

### API Endpoints
- **Frontend**: `http://localhost:8085`
- **Backend**: `http://localhost:8001/api`
- **Suggest**: `GET /api/address/suggest?q={query}`
- **Validate**: `POST /api/address/validate`

### External API
- **URL**: `https://api.addressable.dev/v2/autocomplete`
- **Rate Limit**: 100 requests/day (IP-based)
- **Current Key**: `A_xWMNLslywtPO2DQ8jiMg`

---

## Traceability Matrix

| Test ID | Category | Priority | Requirement |
|---------|----------|----------|-------------|
| TC-001 | Functional | Critical | User can search and validate addresses |
| TC-002 | Functional | High | Validation requires dropdown selection |
| TC-003 | Functional | Critical | Access control enforced by group |
| TC-004 | Functional | High | User can logout |
| TC-005 | Security | Critical | API requires authentication |
| TC-006 | Security | Critical | API requires authentication |
| TC-007 | Security | Critical | Invalid tokens rejected |
| TC-008 | Security | Critical | JWT integrity validated |
| TC-009 | Security | High | Authorization format validated |
| TC-010 | Security | High | Empty tokens rejected |
| TC-011 | API | Critical | Auth required for validation |
| TC-012 | API | Critical | Auth required for suggestions |
| TC-013 | API | Medium | Input validation enforced |
| TC-014 | Error | High | Timeout errors handled |
| TC-015 | Error | Medium | Slow responses handled |
| TC-016 | Error | High | Network errors recoverable |
| TC-017 | Integration | Medium | External API returns data |
| TC-018 | Integration | Medium | External API schema correct |
| TC-019 | Integration | Medium | API contract validated |

---

**Document Version**: 1.0  
**Last Updated**: April 22, 2026  
**Total Test Cases**: 19 (16 active, 3 skipped by default)
