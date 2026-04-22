import logging
import pytest
import requests
from playwright.sync_api import sync_playwright
from config import HEADLESS, SLOW_MO

logger = logging.getLogger(__name__)


def _log_response(response, *args, **kwargs):
    """Requests event hook: logs every HTTP request and its response status."""
    logger.info("%s %s -> %s", response.request.method, response.request.url, response.status_code)


@pytest.fixture(autouse=True)
def http_logging():
    """Attach the response hook to the requests Session for every test."""
    requests.Session.send_original = requests.Session.send

    def patched_send(self, request, **kwargs):
        response = self.send_original(request, **kwargs)
        _log_response(response)
        return response

    requests.Session.send = patched_send
    yield
    requests.Session.send = requests.Session.send_original
    del requests.Session.send_original

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        yield browser
        browser.close()


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
    yield page
    # Cleanup: ensure we're logged out before closing
    try:
        page.goto("http://localhost:8085", timeout=2000, wait_until="domcontentloaded")
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
    except:
        pass  # Ignore cleanup errors
    context.close()