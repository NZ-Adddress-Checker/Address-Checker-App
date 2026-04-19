import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", 0))
TIMEOUT = int(os.getenv("TIMEOUT", 30000))


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser fixture"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Function-scoped context fixture (new context per test)"""
    context = browser.new_context()
    context.set_default_timeout(TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Function-scoped page fixture (new page per test)"""
    page = context.new_page()
    page.set_default_timeout(TIMEOUT)
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page):
    """Authenticated page - user is logged in"""
    # Navigate to login page
    page.goto(BASE_URL)
    page.wait_for_url(f"{BASE_URL}/**", timeout=TIMEOUT)
    
    # Get credentials from environment
    email = os.getenv("TEST_USER_EMAIL", "test-user@example.com")
    password = os.getenv("TEST_USER_PASSWORD", "TestPassword123!")
    
    # Perform login
    # Click on email field and enter credentials
    page.fill('input[name="email"], input[id*="email"], input[placeholder*="email" i]', email)
    page.fill('input[name="password"], input[id*="password"], input[placeholder*="password" i]', password)
    
    # Click sign in button
    page.click('button:has-text("Sign In"), button:has-text("Login"), button:has-text("sign in")')
    
    # Wait for authentication to complete
    page.wait_for_url(f"{BASE_URL}/**", timeout=TIMEOUT)
    
    # Verify JWT token exists in localStorage
    token = page.evaluate("localStorage.getItem('id_token') || localStorage.getItem('token') || localStorage.getItem('jwt')")
    assert token is not None, "JWT token not found in localStorage after login"
    
    yield page


@pytest.fixture(scope="function")
def unauthenticated_page(page):
    """Unauthenticated page - clear localStorage and go to login"""
    page.goto(BASE_URL)
    page.evaluate("localStorage.clear()")
    page.evaluate("sessionStorage.clear()")
    page.reload()
    yield page


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test information"""
    print(f"\n[TEST START] {request.node.name}")
    yield
    print(f"[TEST END] {request.node.name}")
