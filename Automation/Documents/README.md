# NZ Address Checker - Automation Test Suite

## 📋 Overview

Comprehensive test automation framework for the NZ Address Checker application, covering UI, API, security, and integration testing using Playwright and pytest.

## 🎯 Test Coverage

### UI Tests (Playwright)
- ✅ User authentication flow (Login/Logout)
- ✅ Address autocomplete functionality
- ✅ Dropdown suggestion validation
- ✅ Address validation workflow
- ✅ Access control enforcement
- ✅ Error handling scenarios

### API Tests
- ✅ JWT authentication validation
- ✅ Authorization checks
- ✅ Request/response validation
- ✅ Security testing (token tampering, missing auth)
- ✅ Error response handling

### Integration Tests
- ✅ External API contract validation (Addressable API)
- ✅ Backend-Frontend integration
- ✅ Error scenario handling

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker Desktop (for running the application)
- Git

### Installation

```bash
# Clone the repository
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

### Running Tests

```bash
# Run all tests
python -m pytest -v

# Run specific test categories
python -m pytest Tests/test_ui_flow.py -v          # UI tests only
python -m pytest Tests/test_backend_api.py -v      # API tests only
python -m pytest Tests/test_jwt_security.py -v     # Security tests only

# Run with visible browser (for debugging)
python -m pytest --headed -v

# Run specific test
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow -v

# Skip external API tests (to preserve quota)
python -m pytest -m "not external" -v
```

## 📊 Test Reports

HTML reports are automatically generated after each test run:
- **Location**: `report.html`
- **Format**: Self-contained HTML with detailed results
- **Open**: Double-click the file or run `Start-Process report.html`

## 🏗️ Architecture

```
nz-address-checker-automation/
├── Tests/                      # Test files
│   ├── test_ui_flow.py        # UI end-to-end tests
│   ├── test_backend_api.py    # API authentication tests
│   ├── test_jwt_security.py   # Security-specific tests
│   ├── test_address_api.py    # Address endpoint tests
│   └── test_addressable_contract.py  # External API contract tests
├── pages/                      # Page Object Model
│   ├── base_page.py           # Base page class
│   ├── login_page.py          # Login page interactions
│   ├── dashboard_page.py      # Dashboard page interactions
│   └── no_access_page.py      # Access denied page
├── schemas/                    # API schema validation
│   └── addressable_schema.py  # Addressable API schema
├── utils/                      # Utility functions
│   └── jwt_helper.py          # JWT token utilities
├── Documents/                  # Documentation
├── config.py                   # Test configuration
├── conftest.py                # Pytest fixtures
├── pytest.ini                 # Pytest configuration
└── requirements.txt           # Python dependencies
```

## ⚙️ Configuration

Edit `config.py` to customize:
- Base URL (default: `http://localhost:5002`)
- API URL (default: `http://localhost:5001/api`)
- Test user credentials
- API keys
- Browser settings (headless, slow-mo)

## 🔧 Environment Setup

### Application Stack
1. **Frontend**: React app on port 5002
2. **Backend**: FastAPI on port 5001
3. **Authentication**: AWS Cognito

### Starting the Application

```bash
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose up -d
```

### Verify Services

```powershell
# Check frontend
Invoke-WebRequest -Uri "http://localhost:5002" -TimeoutSec 3

# Check backend
Invoke-WebRequest -Uri "http://localhost:5001/api/health" -TimeoutSec 3
```

## 📝 Test Data

### Valid User
- Username: `testapp`
- Password: `Test@1996!`
- Group: `AddressValidators`

### Invalid User
- Username: `jeffcj`
- Password: `Test@1996!`
- Group: None (access denied)

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed debugging guides.

### Common Issues

**Issue**: Playwright browser not found  
**Solution**: Run `python -m playwright install chromium`

**Issue**: Tests timeout waiting for page load  
**Solution**: Ensure Docker containers are running (`docker ps`)

**Issue**: Addressable API rate limit  
**Solution**: External API tests are skipped by default. Use VPN if rate limited.

## 📈 Test Results

**Current Status**: ✅ 13 passed, 3 skipped (in ~43 seconds)

### Test Categories
- API Security: 3 tests
- Backend API: 3 tests  
- JWT Security: 3 tests
- UI Flow: 4 tests
- External API: 3 tests (skipped by default)

## 🔐 Security Testing

The suite includes comprehensive security tests:
- JWT token tampering detection
- Missing authentication handling
- Invalid token rejection
- Authorization bypass attempts
- Group-based access control

## 🌐 External Dependencies

### Addressable API
- **Endpoint**: `https://api.addressable.dev/v2/autocomplete`
- **Rate Limit**: 100 requests/day (free tier, IP-based)
- **Tests**: Marked with `@pytest.mark.external` and skipped by default

To run external tests:
```bash
pytest -m external -v
```

## 📚 Additional Documentation

- [CI/CD Integration Guide](CICD_GUIDE.md) - GitHub Actions & GitLab CI setup and configuration ⭐ NEW
- [Test Plan](TEST_PLAN.md) - Comprehensive test planning with scope, objectives, schedule, and resources
- [Test Strategy](TEST_STRATEGY.md) - Testing objectives, approach, and methodology
- [Test Cases](TEST_CASES.md) - Detailed test case specifications with step-by-step execution
- [Impact Analysis](IMPACT_ANALYSIS.md) - Change impact assessment and deployment risk analysis
- [AWS Deployment Guide](AWS_DEPLOYMENT.md) - ECR and ECS Fargate deployment setup
- [Architecture Guide](ARCHITECTURE.md) - Framework design and technical architecture
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Debugging and problem resolution
- [Quick Start Guide](QUICK_START.md) - 5-minute setup and common commands

## 🤝 Contributing

When adding new tests:
1. Follow the Page Object Model pattern
2. Add proper test markers (`@pytest.mark.*`)
3. Include assertion messages
4. Update test documentation
5. Ensure test isolation (no shared state)

## 📞 Support

For issues or questions, refer to the troubleshooting guide or review test execution logs in `report.html`.
