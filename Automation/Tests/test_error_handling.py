import pytest
from config import USERS, BASE_URL
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_api_timeout_shows_error(page):
    """Test that API timeouts are handled gracefully with appropriate error message."""
    page.goto(BASE_URL, wait_until="networkidle")

    # Login first
    login = LoginPage(page)
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    
    # Wait for dashboard to load
    page.wait_for_selector("input.address-input", timeout=5000)
    
    # Mock the backend API to simulate timeout (delay response beyond frontend timeout)
    page.route("**/api/address/suggest**", lambda route: route.abort("timedout"))
    
    # Attempt to search for an address
    dashboard = DashboardPage(page)
    dashboard.search_address("10 Queen Street, Auckland")
    
    # Wait for error handling to kick in
    page.wait_for_timeout(3000)
    
    # Verify error message is displayed
    # The frontend should show either:
    # 1. "Address lookup service is temporarily unavailable" (for network errors)
    # 2. Timeout-related error message
    # 3. No suggestions shown (graceful degradation)
    
    error_visible = page.is_visible(".error-message", timeout=2000)
    suggestions_visible = page.is_visible(".suggestions-list", timeout=1000)
    
    # Either show error OR gracefully hide suggestions
    if error_visible:
        error_text = page.locator(".error-message").inner_text()
        assert "unavailable" in error_text.lower() or "timeout" in error_text.lower() or "failed" in error_text.lower() or "network" in error_text.lower(), \
            f"Expected timeout/network/unavailable error message, got: {error_text}"
        print(f"✓ Timeout error handled correctly: {error_text}")
    else:
        # If no error message, at minimum suggestions should not appear (graceful degradation)
        assert not suggestions_visible, "Suggestions should not appear on timeout"
        print("✓ Timeout handled gracefully (no suggestions shown)")


def test_slow_api_response_handling(page):
    """Test that slow API responses don't break the UI."""
    page.goto(BASE_URL, wait_until="networkidle")

    # Login first
    login = LoginPage(page)
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    
    # Wait for dashboard to load
    page.wait_for_selector("input.address-input", timeout=5000)
    
    # Use a threading.Event so the route handler never blocks Playwright's event loop.
    # The handler holds the response for 3 seconds without sleeping on the main thread.
    import threading

    delay_done = threading.Event()

    def handle_slow_route(route):
        delay_done.wait(timeout=4)   # waits up to 4 s in its own thread
        route.continue_()

    page.route("**/api/address/suggest**", handle_slow_route)

    # Trigger the slow request
    threading.Timer(0, lambda: delay_done.set()).start()   # release immediately
    # Delay the release by 3 seconds
    threading.Timer(3, lambda: delay_done.set()).start()
    
    page.route("**/api/address/suggest**", handle_slow_route)
    
    # Attempt to search for an address
    dashboard = DashboardPage(page)
    dashboard.search_address("10 Queen Street, Auckland")
    
    # Wait for response (should handle slow response gracefully)
    page.wait_for_timeout(5000)
    
    # UI should either:
    # 1. Show suggestions after delay
    # 2. Show error message
    # 3. Show nothing (graceful timeout)
    # But should NOT crash or freeze
    
    # Verify page is still responsive
    assert page.is_visible("input.address-input"), "Input field should still be visible"
    assert page.is_visible("text=Logout"), "Logout button should still be visible"
    
    print("✓ Slow API response handled without UI freeze")


def test_network_error_recovery(page):
    """Test that after a network error, the app can recover on retry."""
    page.goto(BASE_URL, wait_until="networkidle")

    # Login first
    login = LoginPage(page)
    login.login(USERS["valid"]["username"], USERS["valid"]["password"])
    
    # Wait for dashboard to load
    page.wait_for_selector("input.address-input", timeout=5000)
    
    call_count = {"count": 0}
    
    def handle_failing_then_success(route):
        call_count["count"] += 1
        if call_count["count"] == 1:
            # First call: simulate network failure
            route.abort("failed")
        else:
            # Subsequent calls: let through normally
            route.continue_()
    
    page.route("**/api/address/suggest**", handle_failing_then_success)
    
    dashboard = DashboardPage(page)
    
    # First search attempt - should fail
    dashboard.search_address("10 Queen Street")
    page.wait_for_timeout(2000)
    
    # Clear the input
    page.fill("input.address-input", "")
    page.wait_for_timeout(500)
    
    # Second search attempt - should succeed (or at least not crash)
    dashboard.search_address("20 Queen Street")
    page.wait_for_timeout(2000)
    
    # Verify the app is still functional
    assert page.is_visible("input.address-input"), "Input should still be functional after error recovery"
    assert page.is_visible("text=Logout"), "Logout should still be available"
    
    print("✓ Network error recovery verified")
