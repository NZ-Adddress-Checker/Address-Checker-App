import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, TimeoutError
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", 0))
TIMEOUT = int(os.getenv("TIMEOUT", 30000))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))

# Create screenshot directory
SCREENSHOT_DIR = Path("tests/screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser fixture with error handling"""
    try:
        logger.info(f"Launching browser (headless={HEADLESS}, slow_mo={SLOW_MO}ms)")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO,
                args=["--disable-blink-features=AutomationControlled"]  # Hide automation markers
            )
            yield browser
            logger.info("Closing browser")
            browser.close()
    except Exception as e:
        logger.error(f"Browser launch failed: {str(e)}")
        raise


@pytest.fixture(scope="function")
def context(browser):
    """Function-scoped context fixture with proper cleanup"""
    try:
        logger.info("Creating browser context")
        context = browser.new_context(
            ignore_https_errors=True,
            locale="en-NZ"  # Set locale for NZ address testing
        )
        context.set_default_timeout(TIMEOUT)
        yield context
    except Exception as e:
        logger.error(f"Context creation failed: {str(e)}")
        raise
    finally:
        try:
            logger.info("Closing browser context")
            context.close()
        except Exception as e:
            logger.warning(f"Error closing context: {str(e)}")


@pytest.fixture(scope="function")
def page(context):
    """Function-scoped page fixture with proper cleanup"""
    try:
        logger.info("Creating page")
        page = context.new_page()
        page.set_default_timeout(TIMEOUT)
        
        # Set viewport for consistency
        page.set_viewport_size({"width": 1280, "height": 720})
        
        yield page
    except Exception as e:
        logger.error(f"Page creation failed: {str(e)}")
        raise
    finally:
        try:
            logger.info("Closing page")
            page.close()
        except Exception as e:
            logger.warning(f"Error closing page: {str(e)}")


@pytest.fixture(scope="function")
def authenticated_page(page):
    """
    Authenticated page - user is logged in with proper error handling and retry
    """
    from tests.pages.login_page import LoginPage
    
    email = os.getenv("TEST_USER_EMAIL", "test-user@example.com")
    password = os.getenv("TEST_USER_PASSWORD", "TestPassword123!")
    
    login_success = False
    last_error = None
    
    for attempt in range(RETRY_ATTEMPTS):
        try:
            logger.info(f"Login attempt {attempt + 1}/{RETRY_ATTEMPTS}")
            
            # Navigate to login
            page.goto(BASE_URL, wait_until="networkidle")
            
            # Use LoginPage POM for stable login
            login_page = LoginPage(page)
            
            # Wait for login page to load
            assert login_page.is_login_page_visible(), "Login page not visible"
            
            # Perform login
            login_page.login(email, password)
            
            # Wait for authentication to complete
            page.wait_for_url(f"{BASE_URL}/**", timeout=TIMEOUT, wait_until="networkidle")
            
            # Verify JWT token
            token = page.evaluate(
                "localStorage.getItem('id_token') || localStorage.getItem('token') || localStorage.getItem('jwt')"
            )
            
            assert token is not None, "JWT token not found after login"
            logger.info("Login successful")
            login_success = True
            break
            
        except (AssertionError, TimeoutError) as e:
            last_error = str(e)
            logger.warning(f"Login attempt {attempt + 1} failed: {last_error}")
            
            # Take screenshot for debugging
            screenshot_path = SCREENSHOT_DIR / f"login_failed_attempt_{attempt + 1}.png"
            try:
                page.screenshot(path=str(screenshot_path))
                logger.info(f"Screenshot saved: {screenshot_path}")
                # Also log the current URL and page title for debugging
                logger.info(f"Current URL: {page.url}")
                logger.info(f"Page title: {page.title()}")
            except Exception as screenshot_error:
                logger.warning(f"Failed to save screenshot: {screenshot_error}")
            
            if attempt < RETRY_ATTEMPTS - 1:
                page.goto(BASE_URL, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)  # Wait longer before retry
            continue
    
    if not login_success:
        screenshot_path = SCREENSHOT_DIR / "login_failed_final.png"
        try:
            page.screenshot(path=str(screenshot_path))
            logger.info(f"Final screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.warning(f"Failed to save final screenshot: {e}")
        raise AssertionError(f"Login failed after {RETRY_ATTEMPTS} attempts: {last_error}")
    
    yield page


@pytest.fixture(scope="function")
def unauthenticated_page(page):
    """Unauthenticated page - cleared localStorage"""
    logger.info("Setting up unauthenticated page")
    page.goto(BASE_URL)
    page.evaluate("localStorage.clear()")
    page.evaluate("sessionStorage.clear()")
    page.reload()
    yield page


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test information with detailed output"""
    test_name = request.node.name
    logger.info(f"{'='*70}")
    logger.info(f"TEST START: {test_name}")
    logger.info(f"{'='*70}")
    
    yield
    
    logger.info(f"{'='*70}")
    logger.info(f"TEST END: {test_name}")
    logger.info(f"{'='*70}\n")


@pytest.fixture
def take_screenshot_on_failure(page, request):
    """Take screenshot on test failure"""
    yield
    
    # Check if test failed
    if request.node.rep_call.failed:
        try:
            screenshot_path = SCREENSHOT_DIR / f"{request.node.name}_FAILED.png"
            logger.info(f"Taking screenshot: {screenshot_path}")
            page.screenshot(path=str(screenshot_path), full_page=True)
        except Exception as e:
            logger.warning(f"Failed to take screenshot: {str(e)}")
