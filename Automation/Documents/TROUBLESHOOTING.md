# Troubleshooting Guide - NZ Address Checker Automation

## 🚨 Common Issues & Solutions

### 1. Playwright Browser Not Found

**Error**:
```
playwright._impl._errors.Error: Executable doesn't exist at ...
```

**Cause**: Playwright browsers not installed

**Solution**:
```bash
python -m playwright install chromium
```

**Verification**:
```bash
python -m playwright install --help
```

---

### 2. Tests Timeout Waiting for Page Load

**Error**:
```
playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded
waiting for locator("input[name='username']") to be visible
```

**Possible Causes**:
1. Docker containers not running
2. Frontend/Backend not started
3. Network connectivity issues
4. Cognito redirect failing

**Solutions**:

**Step 1**: Verify containers are running
```powershell
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                    STATUS
...            address-checker-frontend Up 2 hours
...            address-checker-backend  Up 2 hours
```

**Step 2**: Check service health
```powershell
# Check frontend
Invoke-WebRequest -Uri "http://localhost:8085" -TimeoutSec 3

# Check backend
Invoke-WebRequest -Uri "http://localhost:8001/api/health" -TimeoutSec 3
```

**Step 3**: Restart containers if needed
```powershell
docker-compose down
docker-compose up -d
```

**Step 4**: Check Cognito accessibility
- Ensure network connectivity
- VPN might be required for Addressable API
- Cognito URL: https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com

---

### 3. Start Button Click Fails Inconsistently

**Error**:
```
Failed to navigate to Cognito after 5 attempts
```

**Cause**: React OIDC race condition - event handlers not always attached

**Solution**: Already implemented in `login_page.py`

**Current Retry Logic**:
- 5 attempts with URL verification
- Waits for networkidle before clicking
- Validates navigation to Cognito
- Auto-retry if navigation fails

**If Still Failing**:
```python
# Increase wait time in login_page.py
self.wait(2000)  # Instead of 1500
```

---

### 4. Addressable API Rate Limit

**Error**:
```
HTTP 429 Too Many Requests
```

**Cause**: Free tier limit (100 requests/day, IP-based)

**Solutions**:

**Option 1**: Skip external tests (default)
```bash
pytest -m "not external" -v
```

**Option 2**: Use VPN to change IP
```bash
# Connect to VPN, then:
pytest -m external -v
```

**Option 3**: Check current quota
```python
import requests
r = requests.get(
    'https://api.addressable.dev/v2/autocomplete',
    params={'q': 'test', 'country_code': 'NZ', 'api_key': 'YOUR_KEY'}
)
print(r.status_code)  # 200 = quota available, 429 = rate limited
```

---

### 5. Tests Pass But Functionality Broken

**Symptom**: Green checkmarks but dropdown doesn't appear manually

**Cause**: Test not validating actual user-visible behavior

**Verification**:
```python
# Tests should check VISIBLE behavior, not just absence of errors
assert dashboard.has_dropdown(), "Dropdown should be visible"

# NOT just:
assert not dashboard.has_error()  # This can pass even if dropdown missing
```

**Fix**: Tests now include explicit dropdown validation

---

### 6. JWT Token Rejected

**Error**:
```
401 Unauthorized - Invalid token
```

**Causes & Solutions**:

**Cause 1**: Token expired
```python
# Tokens expire after 1 hour
# Solution: Generate fresh token for each test (already implemented)
```

**Cause 2**: Wrong audience
```python
# Ensure CLIENT_ID matches in config
CLIENT_ID = "4p7i1nq2t426jufkh0pe7fgo2u"
```

**Cause 3**: Invalid signature
```python
# Don't tamper with token unless testing security
# Use valid token from actual login
```

---

### 7. Login Fails with Valid Credentials

**Error**:
```
Unable to login with valid credentials
```

**Checklist**:

1. **Verify credentials** in `config.py`:
   ```python
   USERS = {
       "valid": {
           "username": "testapp",
           "password": "Test@1996!"
       }
   }
   ```

2. **Check Cognito user exists**:
   - User: `testapp`
   - Group: `AddressValidators`
   - Status: CONFIRMED

3. **Check for account lockout**:
   - Too many failed attempts can lock account
   - Wait 15 minutes or contact admin

4. **Verify Cognito settings**:
   - Pool ID: `ap-southeast-2_2oQQDAKa4`
   - Client ID: `4p7i1nq2t426jufkh0pe7fgo2u`
   - Region: `ap-southeast-2`

---

### 8. Dropdown Not Appearing

**Possible Causes**:

**Cause 1**: API unavailable
```python
# Test checks for this:
if dashboard.has_error():
    assert "temporarily unavailable" in error_msg
```

**Cause 2**: Rate limit hit
```python
# Solution: Use VPN or wait 24 hours
```

**Cause 3**: Invalid API key
```python
# In config.py, verify:
NZPOST_API_KEY = "A_xWMNLslywtPO2DQ8jiMg"

# In .env file (for backend):
NZPOST_API_KEY=A_xWMNLslywtPO2DQ8jiMg
```

**Cause 4**: Backend not using updated .env
```powershell
# Must REBUILD, not just restart:
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose up --build -d backend
```

---

### 9. Import Errors

**Error**:
```
ModuleNotFoundError: No module named 'playwright'
```

**Solution**:
```bash
# Ensure in correct directory
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"

# Install dependencies
pip install -r requirements.txt
```

**Error**:
```
ImportError: cannot import name 'LoginPage' from 'pages.login_page'
```

**Causes**:
1. Missing `__init__.py` in `pages/` directory
2. Circular imports
3. Case-sensitive imports (Windows vs Linux)

**Solutions**:
1. Verify `pages/__init__.py` exists
2. Check import paths in test files
3. Use consistent casing

---

### 10. Tests Run Slowly

**Current Performance**: ~45 seconds for 13 tests

**Optimization Tips**:

**1. Run specific tests**:
```bash
# Instead of full suite:
pytest -v

# Run only changed tests:
pytest Tests/test_ui_flow.py -v
```

**2. Skip external tests**:
```bash
pytest -m "not external" -v
```

**3. Run in parallel** (future):
```bash
pip install pytest-xdist
pytest -n 4 -v  # 4 workers
```

**4. Use headless mode** (default):
```bash
# Headless is default, but if you changed it:
pytest -v  # Faster
pytest --headed -v  # Slower but visible
```

---

### 11. Permission Denied Errors

**Error**:
```
PermissionError: [WinError 5] Access is denied
```

**Common Causes**:
1. Report file open in browser while running tests
2. Python caching issues
3. File locked by another process

**Solutions**:

**Solution 1**: Close report.html in browser
```powershell
# Close browser tab, then:
pytest -v
```

**Solution 2**: Clear Python cache
```powershell
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\nz-address-checker-automation"
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

**Solution 3**: Run as Administrator (if needed)
```powershell
# Right-click PowerShell → Run as Administrator
```

---

### 12. Environment Variable Not Loaded

**Symptom**: Backend still using old API key after changing `.env`

**Cause**: Docker doesn't reload `.env` on restart

**Solution**:
```powershell
# Must REBUILD:
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose up --build -d backend

# NOT just:
docker-compose restart backend  # This won't work
```

---

## 🔍 Debugging Techniques

### 1. Interactive Debugging

**Playwright Inspector**:
```python
# Add to test where you want to pause:
page.pause()
```

Benefits:
- Step through actions
- Inspect elements
- Try selectors
- View console logs

### 2. Screenshots

**Manual screenshot**:
```python
# Add to test:
page.screenshot(path="debug_screenshot.png")
```

**On failure** (future enhancement):
```python
# In conftest.py fixture
if request.node.rep_call.failed:
    page.screenshot(path=f"failure_{test_name}.png")
```

### 3. Verbose Logging

**Current**:
```bash
pytest -v -s  # -s shows print statements
```

**Future enhancement**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Current URL: %s", page.url)
```

### 4. Network Inspection

**Playwright network logging**:
```python
page.on("request", lambda request: print(f"→ {request.method} {request.url}"))
page.on("response", lambda response: print(f"← {response.status} {response.url}"))
```

### 5. Console Message Capture

```python
page.on("console", lambda msg: print(f"Console: {msg.text}"))
```

---

## 📊 Diagnostic Commands

### System Health Check

```powershell
# Check all components
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker"

# 1. Python version
python --version  # Should be 3.9+

# 2. Playwright installed
python -m playwright --version

# 3. Docker running
docker ps

# 4. Frontend accessible
Invoke-WebRequest -Uri "http://localhost:8085" -TimeoutSec 3

# 5. Backend accessible
Invoke-WebRequest -Uri "http://localhost:8001/api/health" -TimeoutSec 3

# 6. Run smoke test
cd nz-address-checker-automation
pytest Tests/test_ui_flow.py::test_valid_user_flow -v
```

### Test Execution Analysis

```bash
# Run with detailed output
pytest -vv --tb=long

# Show test execution times
pytest --durations=10

# Run specific marker
pytest -m external -v
pytest -m "not external" -v
```

---

## 🆘 Getting Help

### Before Asking for Help

1. ✅ Check this troubleshooting guide
2. ✅ Review test output in `report.html`
3. ✅ Verify all services are running
4. ✅ Check recent code changes
5. ✅ Try running a single test in isolation

### Information to Provide

When reporting issues, include:
- Test name that failed
- Full error message
- Steps to reproduce
- Environment (Python version, OS, Docker status)
- Recent changes made
- Screenshot or video of failure (if UI related)

### Log Files to Check

```powershell
# Backend logs
docker-compose logs backend --tail=50

# Frontend logs
docker-compose logs frontend --tail=50

# Test execution report
# Open: report.html in browser
```

---

## 🔧 Advanced Troubleshooting

### Reset Everything

**Nuclear option** - when nothing else works:

```powershell
# 1. Stop all containers
cd "C:\Users\jeffr\OneDrive\Desktop\NZ add checker\address-checker-app"
docker-compose down

# 2. Clear Docker volumes (WARNING: Deletes data)
docker-compose down -v

# 3. Rebuild from scratch
docker-compose up --build -d

# 4. Reinstall Python dependencies
cd ..\nz-address-checker-automation
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# 5. Reinstall Playwright
python -m playwright install chromium

# 6. Clear Python cache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# 7. Run tests
pytest -v
```

### Debug Specific Component

**Test only authentication**:
```bash
pytest Tests/test_backend_api.py -v
```

**Test only UI**:
```bash
pytest Tests/test_ui_flow.py::test_valid_user_flow --headed -s
```

**Test only security**:
```bash
pytest Tests/test_jwt_security.py -v
```

---

## 📝 Known Issues

### 1. Start Button Race Condition
**Status**: ✅ Fixed  
**Solution**: 5-retry logic with URL verification

### 2. Addressable API Rate Limiting
**Status**: ⚠️ Known Limitation  
**Workaround**: Tests skip by default, use VPN if needed

### 3. Cognito Redirect Timing
**Status**: ✅ Mitigated  
**Solution**: networkidle waits + retry logic

---

## 🎯 Prevention Tips

1. ✅ **Always run smoke test before full suite**
2. ✅ **Keep Docker containers running during dev**
3. ✅ **Don't run external tests unless necessary**
4. ✅ **Check service health before running tests**
5. ✅ **Review report.html after each run**
6. ✅ **Use VPN if testing in region with restricted access**
7. ✅ **Rebuild backend after changing .env**
