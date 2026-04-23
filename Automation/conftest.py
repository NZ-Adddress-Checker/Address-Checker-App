import logging
import pytest
import requests
from playwright.sync_api import sync_playwright
from config import HEADLESS, SLOW_MO

# Ensure the root logger passes INFO records through to pytest's capture handler.
# By default the root logger level is WARNING, which silently drops INFO records
# before they reach any handler — including pytest-html's log capture.
logging.getLogger().setLevel(logging.INFO)

_http_log = logging.getLogger("automation.http")


def pytest_configure(config):
    config.addinivalue_line("markers", "external: marks tests that call external APIs (deselect with '-m not external')")
    config.addinivalue_line("markers", "contract: External API contract tests (skipped by default to preserve quota)")
    config.addinivalue_line("markers", "functional: Functional end-to-end user flow tests")
    config.addinivalue_line("markers", "security: Security and authentication tests")
    config.addinivalue_line("markers", "api: Backend API endpoint tests")
    config.addinivalue_line("markers", "error_handling: Error handling and resilience tests")
    config.addinivalue_line("markers", "smoke: Critical smoke tests for quick validation")
    config.addinivalue_line("markers", "slow: Tests that take longer than 10 seconds")


@pytest.fixture(autouse=True)
def http_logging():
    """Log every requests HTTP call as INFO so pytest-html captures it."""
    original_send = requests.Session.send  # captured in closure — no class-level state

    def patched_send(self, request, **kwargs):
        response = original_send(self, request, **kwargs)
        _http_log.info("%s %s  →  %s", request.method, request.url, response.status_code)
        return response

    requests.Session.send = patched_send
    yield
    requests.Session.send = original_send

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        yield browser
        browser.close()


_pw_log = logging.getLogger("automation.browser")


@pytest.fixture(scope="function")
def page(browser):
    # Create a completely isolated context with no storage state
    context = browser.new_context(
        storage_state=None,  # No cookies/storage from previous tests
        viewport={"width": 1280, "height": 720},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    # Set default timeouts for more reliable interactions
    page.set_default_timeout(30000)  # 30 seconds default timeout
    page.set_default_navigation_timeout(30000)

    # Log every browser network response so pytest captures it in live log / HTML report
    def _on_response(response):
        _pw_log.info("%s %s  →  %s", response.request.method, response.url, response.status)

    page.on("response", _on_response)

    yield page
    # Cleanup: ensure we're logged out before closing
    try:
        page.goto("http://localhost:5002", timeout=2000, wait_until="domcontentloaded")
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
    except:
        pass  # Ignore cleanup errors
    context.close()