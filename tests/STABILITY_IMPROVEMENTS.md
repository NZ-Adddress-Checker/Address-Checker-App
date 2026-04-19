# Test Code Stability & Reusability Improvements

## Overview

This document outlines the comprehensive improvements made to the Playwright automation test framework to make tests more stable, reliable, and reusable.

---

## Key Improvements

### 1. Retry Logic

**Login Fixture (3 Attempts)**
```python
# Login will retry up to 3 times before failing
# Addresses Cognito authentication flakiness
for attempt in range(RETRY_ATTEMPTS):  # Default: 3
    try:
        # Perform login
        # Take screenshot on final failure
```

**Click Operations (3 Attempts)**
```python
# Click with automatic retry
click_element(selector, retry_count=3)
# Waits 500ms between retries
```

**Configurable Retry Helper**
```python
# Use TestHelper for any operation that needs retry
TestHelper.retry_action(
    action=lambda: do_something(),
    max_retries=3,
    wait_ms=500,
    description="Operation name"
)
```

---

### 2. Multiple Selector Strategies

**Login Page Example**
```python
EMAIL_SELECTORS = [
    'input[name="email"]',
    'input[id*="email"]',
    'input[placeholder*="email" i]',
    'input[type="email"]',
]

# Automatically tries each selector until one works
email_selector = self._find_element(self.EMAIL_SELECTORS)
```

**Main Page Example**
```python
SIGN_OUT_SELECTORS = [
    'button:has-text("Sign Out")',
    'button:has-text("Logout")',
    'button:has-text("logout")',
    'a:has-text("Sign Out")',
]

# Falls back to alternative selectors
sign_out_selector = self._find_element(self.SIGN_OUT_SELECTORS)
```

**Benefits**
- Handles UI framework differences
- Supports multiple attribute matching patterns
- Graceful fallback on first selector failure
- More robust across different implementations

---

### 3. Comprehensive Error Handling

**Timeout Fallback**
```python
try:
    page.goto(url, wait_until="networkidle")
except TimeoutError:
    logger.warning("Timeout with networkidle, trying domcontentloaded")
    page.goto(url, wait_until="domcontentloaded")
```

**Element State Validation**
```python
# Wait for specific element state, not just existence
wait_for_element(selector, timeout=5000, state="visible")
# States: 'attached', 'detached', 'visible', 'hidden'
```

**Proper Error Messages**
```python
# Clear, actionable error messages
TestHelper.assert_equals(
    actual=result,
    expected="valid",
    message="Address validation result"
)
# Output: "Address validation result\nExpected: 'valid', Got: 'invalid'"
```

---

### 4. Reusable Helper Classes

**TestHelper**
```python
from tests.utils.helpers import TestHelper

# Retry any action
TestHelper.retry_action(
    action=lambda: click_button(),
    max_retries=3
)

# Wait for condition
TestHelper.wait_for_condition(
    condition=lambda: element.is_visible(),
    timeout_ms=10000
)

# Better assertions
TestHelper.assert_equals(actual, expected)
TestHelper.assert_contains(text, substring)
TestHelper.assert_not_empty(value)
```

**FormHelper**
```python
from tests.utils.helpers import FormHelper

# Fill form field with validation
FormHelper.fill_form_field(page, "#email", "test@example.com")

# Submit form
FormHelper.submit_form(page, "#submit")
```

**NavigationHelper**
```python
from tests.utils.helpers import NavigationHelper

# Navigate and wait for page load
NavigationHelper.navigate_and_wait(
    page,
    "http://localhost:8080",
    wait_until="networkidle"
)

# Check if on page
NavigationHelper.is_on_page(page, "http://localhost:8080/**")
```

**StorageHelper**
```python
from tests.utils.helpers import StorageHelper

# Get JWT token
token = StorageHelper.get_jwt_token(page)

# Manage storage
StorageHelper.set_local_storage(page, "key", "value")
StorageHelper.clear_storage(page)
```

---

### 5. Comprehensive Logging

**Setup**
```python
import logging

logger = logging.getLogger(__name__)

# Automatic test start/end logging
logger.info(f"Starting {test_name}")
logger.debug(f"Detailed operation information")
logger.error(f"Error with context")
```

**Log Levels**
- **INFO**: Test flow, major steps, results
- **DEBUG**: Detailed operations, selector discovery
- **ERROR**: Failures, exceptions with context
- **WARNING**: Timeouts, fallbacks

**Example Test Output**
```
[INFO] Starting SMOKE-001: Valid Login Test
[DEBUG] Login page loaded successfully
[DEBUG] Attempting login with test@example.com
[DEBUG] Page loaded after login
[DEBUG] Sign Out button found - user authenticated
[INFO] SMOKE-001 passed: Valid login successful
```

---

### 6. Screenshot Capture on Failure

**Automatic on Test Failure**
```python
# Screenshots automatically captured to tests/screenshots/
# Filename: {test_name}_FAILED.png

# Manual capture
page.screenshot(path="tests/screenshots/manual.png", full_page=True)
```

**Login Failure**
```python
# If login fails after 3 attempts:
# Screenshot: tests/screenshots/login_failed_*.png
```

**Test Step Failure**
```python
# If test step fails:
# Screenshot: tests/screenshots/{test_name}_FAILED.png
# Used for debugging
```

---

## Stability Features

### Element Waiting Strategies

```python
# Wait for element with specific state
wait_for_element(selector, timeout=5000, state="visible")

# Check visibility without failing
is_visible = is_element_visible(selector, timeout=3000)

# Wait for multiple elements
elements = wait_for_element_count(selector, expected_count=5)
```

### Better Timeout Handling

```python
# Default timeouts
DEFAULT_TIMEOUT = 30000  # 30 seconds
SMALL_TIMEOUT = 3000    # 3 seconds
MEDIUM_TIMEOUT = 5000   # 5 seconds
LARGE_TIMEOUT = 10000   # 10 seconds

# Configurable per operation
wait_for_element(selector, timeout=custom_timeout)
```

### Browser Configuration

```python
# Browser context with safety settings
context = browser.new_context(
    ignore_https_errors=True,
    locale="en-NZ"  # NZ locale for address testing
)

# Browser with automation detection hiding
browser = p.chromium.launch(
    headless=HEADLESS,
    slow_mo=SLOW_MO,
    args=["--disable-blink-features=AutomationControlled"]
)
```

---

## Test Improvements

### Smoke Tests with Stability
- Comprehensive logging at each step
- Screenshot capture on failure
- Helper usage (TestHelper, StorageHelper)
- Better error messages with context
- Detailed assertions with expected vs actual

### Sanity Tests with Stability
- Step-by-step logging (Step 1, Step 2, etc.)
- Failure context preservation
- Screenshot capture on step failure
- Multiple assertion indicators (valid, success, ok, confirmed)
- Clear error messages for debugging

---

## Files Modified

| File | Changes |
|------|---------|
| `conftest.py` | Retry logic, logging, error handling |
| `pages/base_page.py` | Multiple selectors, retry logic, logging |
| `pages/login_page.py` | Selector discovery, error handling |
| `pages/main_page.py` | Selector discovery, error handling |
| `utils/helpers.py` | **NEW** - Reusable helper classes |
| `smoke/test_smoke.py` | Logging, helpers, better assertions |
| `sanity/test_sanity.py` | Logging, helpers, better assertions |

---

## Usage Examples

### Example 1: Using Retry Logic
```python
from tests.utils.helpers import TestHelper

# Retry a flaky operation
result = TestHelper.retry_action(
    action=lambda: page.click("#button"),
    max_retries=3,
    description="Button click"
)
```

### Example 2: Using Helpers in Tests
```python
from tests.utils.helpers import TestHelper, StorageHelper

# Check if logged in
token = StorageHelper.get_jwt_token(page)
TestHelper.assert_not_empty(token, "JWT token required")

# Retry assertion
TestHelper.retry_action(
    action=lambda: assert_equals(result, "valid"),
    max_retries=3
)
```

### Example 3: Multiple Selectors
```python
# Page objects automatically try multiple selectors
main_page = MainPage(page)

# This tries: button:has-text("Sign Out"), then "Sign Out", then "Logout", etc.
main_page.sign_out()

# Uses first working selector automatically
```

### Example 4: Better Error Messages
```python
# Clear, actionable error messages
try:
    TestHelper.assert_contains(result, "valid")
except AssertionError as e:
    # Error message: "'invalid address' does not contain 'valid'"
    # Much clearer than simple assert failure
```

---

## Benefits Summary

| Aspect | Benefit |
|--------|---------|
| **Stability** | Retry logic handles transient failures |
| **Flexibility** | Multiple selectors handle UI variations |
| **Debugging** | Comprehensive logging and screenshots |
| **Reusability** | Helper classes for common operations |
| **Maintainability** | Clear error messages and context |
| **Scalability** | Easy to add new tests with helpers |
| **Reliability** | Better timeout handling and fallbacks |
| **Speed** | No unnecessary waits, smart retries |

---

## Configuration

### Environment Variables
```bash
# Browser
HEADLESS=false          # Show browser during tests
SLOW_MO=0              # Delay between actions (ms)

# Timeouts
TIMEOUT=30000          # Default timeout (ms)

# Retry
RETRY_ATTEMPTS=3       # Login retry attempts
```

### Logging
```python
# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Get logger
logger = logging.getLogger(__name__)
logger.info("Message")
logger.debug("Debug info")
logger.error("Error occurred")
```

---

## Best Practices

1. **Use Helpers**: Use provided helper classes instead of direct Playwright calls
2. **Log Liberally**: Add logging for debugging and troubleshooting
3. **Take Screenshots**: Screenshots help diagnose UI issues
4. **Retry Flaky Ops**: Use retry logic for operations that may fail transiently
5. **Clear Assertions**: Use TestHelper assertions for better error messages
6. **Multiple Selectors**: Add multiple selectors for page objects to handle variations
7. **Proper Cleanup**: Always use fixtures and context managers
8. **Test Independence**: Each test should be independent and repeatable

---

## Future Enhancements

- [ ] Video recording on test failure
- [ ] Parallel test execution
- [ ] HTML report generation
- [ ] Performance metrics collection
- [ ] Visual regression testing
- [ ] API testing integration
- [ ] Cross-browser testing
- [ ] Accessibility testing

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19  
**Status**: Production Ready
