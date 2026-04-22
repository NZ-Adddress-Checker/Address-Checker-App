# Architecture Documentation - Test Automation Framework

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Automation Framework                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   UI     │  │   API    │  │ Security │  │External  │   │
│  │  Tests   │  │  Tests   │  │  Tests   │  │API Tests │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │              │          │
│  ┌────▼─────────────▼──────────────▼──────────────▼─────┐  │
│  │              Test Infrastructure                       │  │
│  │  (Fixtures, Utilities, Page Objects, Schemas)         │  │
│  └────────────────────────────┬───────────────────────────┘  │
└────────────────────────────────┼──────────────────────────────┘
                                 │
                     ┌───────────▼───────────┐
                     │   Application Stack    │
                     │ (Frontend + Backend)   │
                     └───────────────────────┘
```

## 📁 Directory Structure

```
nz-address-checker-automation/
│
├── Tests/                          # Test Files (Test Layer)
│   ├── test_ui_flow.py            # UI end-to-end tests
│   ├── test_backend_api.py        # Backend API tests
│   ├── test_jwt_security.py       # Security-focused tests
│   ├── test_address_api.py        # Address endpoint tests
│   └── test_addressable_contract.py # External API contract tests
│
├── pages/                          # Page Object Model (Abstraction Layer)
│   ├── base_page.py               # Base page with common methods
│   ├── login_page.py              # Login page interactions
│   ├── dashboard_page.py          # Dashboard page interactions
│   └── no_access_page.py          # Access denied page
│
├── utils/                          # Utility Functions (Helper Layer)
│   └── jwt_helper.py              # JWT token manipulation
│
├── schemas/                        # Schema Validation (Validation Layer)
│   └── addressable_schema.py      # API response schemas
│
├── Documents/                      # Documentation
│   ├── README.md                  # Main documentation
│   ├── TEST_STRATEGY.md           # Testing strategy
│   ├── ARCHITECTURE.md            # This file
│   ├── TROUBLESHOOTING.md         # Debug guide
│   └── QUICK_START.md             # Getting started guide
│
├── config.py                       # Configuration (Config Layer)
├── conftest.py                     # Pytest fixtures (Infrastructure Layer)
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore patterns
└── report.html                     # Generated test report
```

## 🎭 Layer Architecture

### 1. Test Layer (`Tests/`)
**Purpose**: Define test scenarios and assertions

**Responsibilities**:
- Execute test scenarios
- Make assertions
- Orchestrate page objects
- Validate API responses

**Example**:
```python
def test_valid_user_flow(page):
    """Test that valid user can search and validate addresses"""
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    
    # Arrange
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    
    # Act
    dashboard.search_address("10 Queen Street, Auckland")
    
    # Assert
    assert dashboard.has_dropdown(), "Dropdown should appear with suggestions"
```

### 2. Page Object Layer (`pages/`)
**Purpose**: Abstract UI interactions from test logic

**Design Pattern**: Page Object Model (POM)

**Base Page Hierarchy**:
```
BasePage
  ├── LoginPage
  ├── DashboardPage
  └── NoAccessPage
```

**Base Page Features**:
- Common navigation methods
- Generic wait strategies
- Element interaction utilities
- Error handling

**Example**:
```python
class BasePage:
    def __init__(self, page):
        self.page = page
    
    def click(self, selector):
        self.page.click(selector)
    
    def fill(self, selector, value):
        self.page.fill(selector, value)
    
    def wait(self, ms):
        self.page.wait_for_timeout(ms)
```

### 3. Utility Layer (`utils/`)
**Purpose**: Reusable helper functions

**Current Utilities**:
- `jwt_helper.py`: JWT token creation, manipulation, tampering

**Usage**:
```python
from utils.jwt_helper import create_tampered_token

# Create invalid token for security testing
bad_token = create_tampered_token(valid_token)
```

### 4. Schema Layer (`schemas/`)
**Purpose**: Validate API response structures

**Pattern**: Schema definition + validation

**Example**:
```python
# schemas/addressable_schema.py
ADDRESSABLE_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "formatted": {"type": "string"},
        "components": {"type": "object"}
    },
    "required": ["formatted"]
}
```

### 5. Configuration Layer (`config.py`)
**Purpose**: Centralize test configuration

**Contents**:
- Application URLs
- API endpoints
- Test user credentials
- API keys
- Browser settings

**Example**:
```python
BASE_URL = "http://localhost:8085"
API_URL = "http://localhost:8001/api"
USERS = {
    "valid": {"username": "testapp", "password": "Test@1996!"}
}
```

### 6. Infrastructure Layer (`conftest.py`)
**Purpose**: Pytest fixtures and test setup

**Fixtures**:
- `browser`: Playwright browser instance
- `page`: Fresh page with clean state per test

**Key Features**:
- Browser context isolation
- LocalStorage cleanup
- Default timeouts
- User agent configuration

**Example**:
```python
@pytest.fixture
def page(browser):
    context = browser.new_context(
        storage_state=None,  # Clean state
        viewport={'width': 1280, 'height': 720}
    )
    page = context.new_page()
    page.set_default_timeout(30000)
    
    yield page
    
    # Cleanup
    page.evaluate("localStorage.clear()")
    context.close()
```

## 🔄 Test Execution Flow

### UI Test Flow
```
1. Pytest starts
   ↓
2. conftest.py creates browser fixture
   ↓
3. Fresh page context created
   ↓
4. Test imports page objects
   ↓
5. Page objects interact with browser
   ↓
6. Test makes assertions
   ↓
7. Fixture cleanup (localStorage.clear())
   ↓
8. Report generation
```

### API Test Flow
```
1. Pytest starts
   ↓
2. Test creates JWT token (or uses invalid token)
   ↓
3. Make HTTP request with token
   ↓
4. Validate response status
   ↓
5. Validate response schema (if success)
   ↓
6. Assert expected behavior
```

## 🔌 Integration Points

### Application Under Test
```
┌────────────────────────────────────────┐
│         Test Framework                 │
└───────────┬────────────────────────────┘
            │
            ├──── HTTP ───→ Frontend (Port 8085)
            │                   │
            │                   │ HTTPS
            │                   ↓
            │              AWS Cognito
            │                   │
            │                   ↓
            └──── HTTP ───→ Backend (Port 8001)
                               │
                               │ HTTPS
                               ↓
                          Addressable API
```

### Test Dependencies
```
pytest (8.4.2)
  ├── pytest-playwright (0.7.1)
  │     └── playwright (1.47.0)
  │           └── chromium-1134
  ├── pytest-html (4.2.0)
  ├── requests (2.31.0)
  ├── jsonschema (4.23.0)
  └── python-jose (3.3.0)
```

## 🎯 Design Patterns

### 1. Page Object Model (POM)
**Benefits**:
- ✅ Encapsulation of page structure
- ✅ Reusability across tests
- ✅ Easy maintenance
- ✅ Reduced code duplication

**Example**:
```python
# Instead of this in tests:
page.click("text=Start")
page.fill("input[name='username']", "testapp")
page.click("button[type='submit']")

# We have this:
login_page.login("testapp", "password")
```

### 2. Fixture Pattern
**Benefits**:
- ✅ Setup/teardown automation
- ✅ Test isolation
- ✅ Resource management
- ✅ Dependency injection

### 3. AAA Pattern (Arrange-Act-Assert)
**Structure**:
```python
def test_example():
    # Arrange: Set up test data and state
    login = LoginPage(page)
    user = USERS["valid"]
    
    # Act: Perform the action being tested
    login.login(user["username"], user["password"])
    
    # Assert: Verify expected outcome
    assert page.url.contains("/dashboard")
```

### 4. Builder Pattern (Future)
**Planned for test data**:
```python
# Future enhancement
user = UserBuilder()
    .with_username("testapp")
    .with_group("AddressValidators")
    .build()
```

## 🛡️ Error Handling Strategy

### Retry Logic
**Location**: `pages/login_page.py`

**Pattern**:
```python
max_retries = 5
for attempt in range(max_retries):
    try:
        # Attempt action
        with page.expect_navigation(timeout=10000):
            page.click(BUTTON)
        
        # Verify success
        if "cognito" in page.url:
            break
    except Exception as e:
        if attempt < max_retries - 1:
            # Retry
            page.goto(BASE_URL)
        else:
            raise
```

### Conditional Validation
**Pattern**: Handle variable states
```python
if dashboard.has_error():
    # Validate error scenario
    assert "unavailable" in dashboard.get_error_message()
else:
    # Validate success scenario
    assert dashboard.has_dropdown()
```

## 📊 Reporting Architecture

### HTML Report Generation
**Tool**: pytest-html plugin

**Configuration**:
```ini
# pytest.ini
[pytest]
addopts = -v --html=report.html --self-contained-html
```

**Output**:
- Self-contained HTML file
- Execution timestamps
- Pass/fail status
- Error tracebacks
- Execution duration

## 🔐 Security Architecture

### JWT Validation Tests
**Approach**:
1. Generate valid JWT token
2. Tamper with token (modify signature, payload, or headers)
3. Send to API
4. Verify rejection with 401 status

### Authentication Flow
```
Test → Cognito Hosted UI → Username/Password
                              ↓
                         Authorization Code
                              ↓
                          Token Exchange
                              ↓
                         JWT ID Token
                              ↓
                      Backend Validation
                              ↓
                    JWKS Key Verification
```

## 🚀 Performance Considerations

### Current Performance
- **Total Suite**: ~45 seconds (13 tests)
- **Average per test**: ~3.5 seconds
- **UI tests**: ~10 seconds each (includes Cognito redirects)
- **API tests**: ~1 second each

### Optimization Opportunities
1. **Parallel Execution** (pytest-xdist)
   - Potential: 50% reduction with 4 workers
   
2. **Selective Test Runs**
   - Run only affected tests based on code changes
   
3. **Cached Authentication**
   - Reuse tokens across API tests (currently fresh each time)

## 🔄 Extensibility

### Adding New Test Types
1. Create new test file: `Tests/test_new_feature.py`
2. Import required page objects or utilities
3. Follow AAA pattern
4. Add markers if needed (`@pytest.mark.feature`)

### Adding New Page Objects
1. Create file in `pages/new_page.py`
2. Inherit from `BasePage`
3. Define selectors as class constants
4. Implement interaction methods

### Adding New Utilities
1. Create file in `utils/new_helper.py`
2. Define reusable functions
3. Add type hints
4. Document usage with docstrings

## 🎓 Best Practices Enforced

1. ✅ **Test Isolation**: Each test has fresh browser context
2. ✅ **DRY Principle**: Page objects prevent duplication
3. ✅ **Single Responsibility**: Each file has one clear purpose
4. ✅ **Configuration Management**: Centralized in `config.py`
5. ✅ **Clean Code**: PEP 8 compliance, type hints where beneficial
6. ✅ **Documentation**: Comprehensive docs in `Documents/`

## 🔍 Debugging Tools

### Built-in Debugging
```python
# Add to test for debugging
page.pause()  # Opens Playwright inspector
```

### Logging (Future Enhancement)
```python
# Planned
import logging
logger = logging.getLogger(__name__)
logger.info("Starting login process")
```

### Screenshot Capture (Future)
```python
# Planned
page.screenshot(path="failure_screenshot.png")
```

## 📈 Scalability Roadmap

### Phase 1 (Current)
- ✅ Core test coverage
- ✅ Page Object Model
- ✅ HTML reporting

### Phase 2 (Next 3 months)
- 🔮 CI/CD integration
- 🔮 Parallel execution
- 🔮 Enhanced logging

### Phase 3 (6+ months)
- 🔮 Visual regression testing
- 🔮 Performance benchmarks
- 🔮 Cross-browser support
- 🔮 API mocking layer
