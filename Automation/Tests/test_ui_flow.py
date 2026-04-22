from config import USERS, BASE_URL
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.no_access_page import NoAccessPage


def test_valid_user_flow(page):
    """Test that a valid user can log in, search address, and handle suggestions or API unavailability."""
    page.goto(BASE_URL, wait_until="networkidle")

    login = LoginPage(page)
    dash = DashboardPage(page)

    login.login(USERS["valid"]["username"], USERS["valid"]["password"])

    # Verify we're on the dashboard
    page.wait_for_selector("input.address-input", timeout=5000)
    assert page.is_visible("text=Logout"), "Should see Logout button on dashboard"

    # Search for an address
    dash.search_address("10 Queen Street, Auckland")
    
    # Wait longer for suggestions to appear (debounce + API call)
    page.wait_for_timeout(2000)
    
    # Check if dropdown suggestions appeared
    dropdown_visible = page.is_visible(".suggestions-list", timeout=2000)
    
    if not dropdown_visible:
        # Check if there's an error message
        if page.is_visible(".error-message"):
            error_text = page.locator(".error-message").inner_text()
            # If it's the API unavailability error, verify the error is shown correctly
            if "temporarily unavailable" in error_text.lower() or "rate limit" in error_text.lower():
                # This is expected behavior when API is rate-limited
                assert not page.is_visible(".suggestions-list"), "Suggestions should NOT appear when API is unavailable"
                assert "temporarily unavailable" in error_text.lower() or "rate limit" in error_text.lower(), \
                    f"Expected API unavailability error message, got: {error_text}"
                print(f"✓ API unavailable scenario verified: {error_text}")
                return  # Test passes - we verified the error handling works
            else:
                raise AssertionError(f"Unexpected error on dashboard: {error_text}")
        else:
            raise AssertionError("Dropdown suggestions did not appear and no error message was shown.")
    
    # If we get here, dropdown appeared - test the full flow
    dash.select_first()
    dash.validate()
    
    # Check if validation succeeded
    assert dash.is_valid(), "Validation should show 'Valid: Yes ✓' after selecting from dropdown"


def test_validation_requires_dropdown_selection(page):
    """Test that validation fails with error message when user doesn't select from dropdown."""
    page.goto(BASE_URL, wait_until="networkidle")

    login = LoginPage(page)
    dash = DashboardPage(page)

    login.login(USERS["valid"]["username"], USERS["valid"]["password"])

    # Type random text without selecting from dropdown
    dash.search_address("random text")
    dash.wait(500)  # Wait a bit to ensure suggestions could appear
    
    # Try to validate without selecting from dropdown
    dash.validate()
    
    # Should show error message
    error_message = page.locator("text=Please select an address from the dropdown list.")
    assert error_message.is_visible(), "Should show error when validating without selecting from dropdown"


def test_invalid_user_blocked(page):

    page.goto(BASE_URL, wait_until="networkidle")

    login = LoginPage(page)
    no_access = NoAccessPage(page)

    login.login(USERS["invalid"]["username"], USERS["invalid"]["password"])

    assert no_access.shown()


def test_logout(page):

    page.goto(BASE_URL, wait_until="networkidle")

    login = LoginPage(page)
    dash = DashboardPage(page)

    login.login(USERS["valid"]["username"], USERS["valid"]["password"])

    dash.logout()

    assert "Start" in page.content()