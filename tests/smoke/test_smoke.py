"""
Smoke Tests for NZ Address Checker Application
Smoke tests verify basic application functionality and critical paths
These tests are stable and reusable with proper error handling and logging
"""
import pytest
import logging
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage
from tests.utils.test_data import TestData
from tests.utils.helpers import TestHelper, StorageHelper, NavigationHelper

logger = logging.getLogger(__name__)


class TestSmokeLogin:
    """Smoke tests for login functionality (TC-AUTH-001)"""
    
    def test_smoke_valid_login(self, page: Page):
        """
        SMOKE-001: User successfully logs in with valid credentials
        Verifies: Authentication works, user can access main page
        Stability: Retry logic, multiple selectors, proper waits
        """
        logger.info("Starting SMOKE-001: Valid Login Test")
        
        # Arrange
        login_page = LoginPage(page)
        credentials = TestData.get_login_credentials()
        
        # Act - Navigate
        login_page.navigate()
        assert login_page.is_login_page_visible(), "Login page should be visible"
        logger.debug("Login page loaded successfully")
        
        # Act - Login
        logger.debug(f"Attempting login with {credentials['email']}")
        login_page.login(credentials["email"], credentials["password"])
        
        # Assert - Verify authentication
        main_page = MainPage(page)
        page.wait_for_url("http://localhost:8080/**", timeout=30000, wait_until="domcontentloaded")
        logger.debug("Page loaded after login")
        
        assert main_page.is_authenticated(), "User should be authenticated (Sign Out button visible)"
        logger.debug("Sign Out button found - user authenticated")
        
        # Assert - Verify JWT token
        token = StorageHelper.get_jwt_token(page)
        TestHelper.assert_not_empty(token, "JWT token should exist in localStorage")
        logger.info("SMOKE-001 passed: Valid login successful")


class TestSmokeAddressSuggestions:
    """Smoke tests for address suggestions (TC-ADDR-001)"""
    
    def test_smoke_address_suggestions(self, authenticated_page: Page):
        """
        SMOKE-002: Address suggestions display for partial input
        Verifies: Autocomplete API works, suggestions dropdown appears
        Stability: Multiple selector strategies, timeout handling
        """
        logger.info("Starting SMOKE-002: Address Suggestions Test")
        
        # Arrange
        main_page = MainPage(authenticated_page)
        test_address = TestData.PARTIAL_ADDRESS
        logger.debug(f"Testing with address: {test_address}")
        
        # Act - Enter address
        main_page.enter_address(test_address)
        logger.debug(f"Entered address: {test_address}")
        
        # Act - Wait for suggestions (with stability)
        try:
            main_page.wait_for_suggestions(timeout=5000)
            logger.debug("Suggestions dropdown appeared")
        except AssertionError as e:
            logger.error(f"Suggestions failed to appear: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/smoke_002_suggestions_failed.png")
            raise
        
        # Assert - Get suggestions
        try:
            suggestions = main_page.get_suggestions()
            assert len(suggestions) > 0, f"Should have suggestions for '{test_address}'"
            logger.info(f"SMOKE-002 passed: Found {len(suggestions)} suggestions")
        except AssertionError as e:
            logger.error(f"No suggestions found: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/smoke_002_no_suggestions.png")
            raise


class TestSmokeAddressValidation:
    """Smoke tests for address validation (TC-VAL-001)"""
    
    def test_smoke_valid_address_validation(self, authenticated_page: Page):
        """
        SMOKE-003: Valid address passes validation
        Verifies: Validation API works, returns valid result
        Stability: Proper waits, result text validation
        """
        logger.info("Starting SMOKE-003: Valid Address Validation Test")
        
        # Arrange
        main_page = MainPage(authenticated_page)
        test_address = TestData.VALID_ADDRESS
        logger.debug(f"Testing with address: {test_address}")
        
        # Act - Enter address
        main_page.enter_address(test_address)
        logger.debug(f"Entered address: {test_address}")
        
        # Act - Click validate
        main_page.click_validate()
        logger.debug("Clicked validate button")
        
        # Wait for validation result (with stability)
        try:
            main_page.wait_for_validation_result(timeout=10000)
            logger.debug("Validation result appeared")
        except AssertionError as e:
            logger.error(f"Validation result timeout: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/smoke_003_validation_timeout.png")
            raise
        
        # Assert - Get and validate result
        try:
            result = main_page.get_validation_result()
            TestHelper.assert_not_empty(result, "Validation result message should be displayed")
            
            # Check for success indicators
            result_lower = result.lower()
            assert any(indicator in result_lower for indicator in ["valid", "success", "ok", "confirmed"]), \
                f"Result should indicate valid address, got: {result}"
            
            logger.info(f"SMOKE-003 passed: Validation result - {result}")
        except AssertionError as e:
            logger.error(f"Validation result assertion failed: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/smoke_003_result_validation.png")
            raise

