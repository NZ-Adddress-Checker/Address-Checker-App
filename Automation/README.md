# NZ Address Checker - Test Automation

[![Tests](https://img.shields.io/badge/tests-19%20automated-brightgreen)](Documents/TEST_CASES.md)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](Documents/TEST_STRATEGY.md)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-ready-blue)](Documents/CICD_GUIDE.md)
[![Framework](https://img.shields.io/badge/framework-Playwright%20%2B%20Pytest-orange)](https://playwright.dev)

Professional test automation framework for the NZ Address Checker application using Playwright and pytest.

**✨ Now CI/CD Ready!** Pre-configured pipelines for GitHub Actions & GitLab CI - see [CI/CD Guide](Documents/CICD_GUIDE.md)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
python -m playwright install chromium

# Run tests
python -m pytest -v

# View report
Start-Process report.html
```

## 📊 Current Status

✅ **16 passed**, 3 skipped in ~92 seconds  
✅ **100% test coverage** (19/19 documented scenarios)  
✅ **CI/CD pipelines** configured and ready  
✅ **Production ready** with comprehensive documentation

## 📚 Documentation

- **[Quick Start Guide](Documents/QUICK_START.md)** - Get up and running in 5 minutes
- **[CI/CD Guide](Documents/CICD_GUIDE.md)** - GitHub Actions & GitLab CI integration ⭐ NEW
- **[Complete README](Documents/README.md)** - Full documentation and usage
- **[Test Plan](Documents/TEST_PLAN.md)** - Comprehensive test planning with scope, objectives, and resources
- **[Test Cases](Documents/TEST_CASES.md)** - Detailed test specifications with step-by-step execution
- **[Impact Analysis](Documents/IMPACT_ANALYSIS.md)** - Change impact assessment and deployment risk analysis
- **[Test Strategy](Documents/TEST_STRATEGY.md)** - Testing approach and methodology
- **[Architecture Guide](Documents/ARCHITECTURE.md)** - Framework design and patterns
- **[Troubleshooting](Documents/TROUBLESHOOTING.md)** - Debug guide and solutions

## 🎯 Test Coverage

- ✅ UI end-to-end flows (4 tests)
- ✅ API authentication (3 tests)
- ✅ JWT security (3 tests)
- ✅ Backend validation (3 tests)
- ⏭️ External API contracts (3 tests - skipped by default)

## 🏗️ Architecture

```
Tests/          # Test files
pages/          # Page Object Model
utils/          # Helper functions
schemas/        # API validation
Documents/      # Comprehensive docs
config.py       # Configuration
conftest.py     # Pytest fixtures
```

## 🔧 Common Commands

```bash
# Run all tests
python -m pytest -v

# Run specific category
python -m pytest Tests/test_ui_flow.py -v

# Run with visible browser
python -m pytest --headed -v

# Skip external API tests
python -m pytest -m "not external" -v
```

## 📖 Learn More

Start with the [Quick Start Guide](Documents/QUICK_START.md) for a guided walkthrough, or dive into the [Complete README](Documents/README.md) for full details.