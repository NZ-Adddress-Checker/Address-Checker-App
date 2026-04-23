# Quick Start Guide - NZ Address Checker Automation

## ⚡ 5-Minute Setup

### Prerequisites Checklist
- [ ] Python 3.9 or higher installed
- [ ] Docker Desktop installed and running
- [ ] Git installed (optional)
- [ ] Windows PowerShell or Command Prompt

### Step 1: Start the Application (2 minutes)

```powershell
# Navigate to application directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"

# Start Docker containers
docker-compose up -d

# Wait 30 seconds for services to start
Start-Sleep -Seconds 30

# Verify services are running
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                             STATUS
...            address-checker-app-frontend...   Up
...            address-checker-app-backend...    Up
```

### Step 2: Install Test Dependencies (2 minutes)

```powershell
# Navigate to automation directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"

# Install Python packages
pip install -r requirements.txt

# Install Playwright browser
python -m playwright install chromium
```

### Step 3: Run Your First Test (1 minute)

```powershell
# Run a single smoke test
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow -v
```

Expected output:
```
Tests/test_ui_flow.py::test_valid_user_flow PASSED [100%]
```

✅ **Success!** If you see `PASSED`, you're all set!

---

## 🎯 Common Test Commands

### Run All Tests
```powershell
python -m pytest -v
```

### Run Specific Test Categories

**UI Tests Only**:
```powershell
python -m pytest Tests/test_ui_flow.py -v
```

**API Tests Only**:
```powershell
python -m pytest Tests/test_backend_api.py -v
```

**Security Tests Only**:
```powershell
python -m pytest Tests/test_jwt_security.py -v
```

### Run With Visible Browser

```powershell
python -m pytest --headed -v
```

### View Test Report

```powershell
# Report is auto-generated after each run
Start-Process report.html
```

---

## 📁 Project Structure at a Glance

```
nz-address-checker-automation/
├── Tests/              # Your test files
│   ├── test_ui_flow.py        # End-to-end UI tests
│   ├── test_backend_api.py    # API tests
│   └── test_jwt_security.py   # Security tests
├── pages/              # Page objects (UI abstraction)
├── config.py           # Configuration (URLs, credentials)
├── report.html         # Latest test report
└── Documents/          # Full documentation
```

---

## 🔧 Troubleshooting Quick Fixes

### Problem: "Module not found"
```powershell
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "Executable doesn't exist"
```powershell
# Solution: Install Playwright browser
python -m playwright install chromium
```

### Problem: "Timeout waiting for page"
```powershell
# Solution: Verify services are running
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose up -d

# Check health
Invoke-WebRequest -Uri "http://localhost:5002" -TimeoutSec 3
Invoke-WebRequest -Uri "http://localhost:5001/api/health" -TimeoutSec 3
```

### Problem: Tests are slow
```powershell
# Solution: Run specific tests instead of full suite
python -m pytest Tests/test_ui_flow.py::test_valid_user_flow -v
```

---

## 📚 Next Steps

### Learn More
1. Read [README.md](README.md) for comprehensive documentation
2. Review [TEST_STRATEGY.md](TEST_STRATEGY.md) to understand testing approach
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed problem solving

### Modify Tests
1. **Change test data**: Edit `config.py`
2. **Add new tests**: Create file in `Tests/` folder
3. **Update UI interactions**: Modify files in `pages/` folder

### Run Tests Your Way

**Quick Smoke Test** (30 seconds):
```powershell
pytest Tests/test_ui_flow.py::test_valid_user_flow -v
```

**Full Regression** (~45 seconds):
```powershell
pytest -v
```

**Debug Mode** (visible browser):
```powershell
pytest --headed -s -v
```

---

## 🎓 Understanding Test Output

### Successful Test Run
```
Tests/test_ui_flow.py::test_valid_user_flow PASSED         [100%]
=============== 1 passed in 10.23s ===============
```

- ✅ `PASSED`: Test successful
- `[100%]`: Progress indicator
- `in 10.23s`: Execution time

### Failed Test Run
```
Tests/test_ui_flow.py::test_valid_user_flow FAILED         [100%]

FAILED Tests/test_ui_flow.py::test_valid_user_flow
AssertionError: Dropdown should be visible
```

- ❌ `FAILED`: Test failed
- Error message explains what went wrong
- Check `report.html` for full details

---

## 🔄 Daily Workflow

### Before Making Changes
```powershell
# 1. Ensure services are running
docker ps

# 2. Run smoke test
pytest Tests/test_ui_flow.py::test_valid_user_flow -v
```

### After Making Changes
```powershell
# 1. Run relevant tests
pytest Tests/test_ui_flow.py -v

# 2. Check report
Start-Process report.html
```

### Before Deployment
```powershell
# Run full test suite
pytest -v

# Verify all passed
# Check report.html for details
```

---

## 💡 Pro Tips

### Tip 1: Speed Up Test Runs
```powershell
# Run only what you need
pytest Tests/test_backend_api.py::test_suggest_requires_auth -v
```

### Tip 2: Debug Failing Tests
```powershell
# Add to your test temporarily:
page.pause()  # Opens Playwright inspector
```

### Tip 3: Keep Services Running
```powershell
# Don't stop Docker between test runs
# Faster test execution
docker ps  # Should show containers running
```

### Tip 4: Skip External API Tests
```powershell
# Saves API quota
pytest -m "not external" -v
```

### Tip 5: View Console Output
```powershell
# See print statements and logs
pytest -s -v
```

---

## 🎯 Your First Custom Test

Create a new test in `Tests/test_my_feature.py`:

```python
from config import BASE_URL
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_my_feature(page):
    """Test description"""
    # Arrange
    page.goto(BASE_URL, wait_until="networkidle")
    
    # Act
    # Your test steps here
    
    # Assert
    assert True, "Test passed!"
```

Run it:
```powershell
pytest Tests/test_my_feature.py::test_my_feature -v
```

---

## 📞 Need Help?

1. **Quick answers**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Understanding architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Test strategy**: See [TEST_STRATEGY.md](TEST_STRATEGY.md)
4. **Full guide**: Review [README.md](README.md)

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Docker containers running (`docker ps`)
- [ ] Frontend accessible (http://localhost:5002)
- [ ] Backend accessible (http://localhost:5001/api/health)
- [ ] Python packages installed (`pip list | findstr playwright`)
- [ ] Playwright browser installed (`python -m playwright --version`)
- [ ] Smoke test passes (`pytest Tests/test_ui_flow.py::test_valid_user_flow -v`)
- [ ] Report generated (`report.html` exists)

---

**🎉 You're ready to go!** Start testing with confidence.
