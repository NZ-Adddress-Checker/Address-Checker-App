"""
Smoke Tests for NZ Address Checker Application
Smoke tests verify basic application functionality and critical paths
"""
import pytest
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage
from tests.utils.test_data import TestData


class TestSmokeLogin:
    """Smoke tests for login functionality (TC-AUTH-001)"""
    
    def test_smoke_valid_login(self, page: Page):
        """
        SMOKE-001: User successfully logs in with valid credentials
        Verifies: Authentication works, user can access main page
        """
        # Arrange
        login_page = LoginPage(page)
        credentials = TestData.get_login_credentials()
        
        # Act
        login_page.navigate()
        assert login_page.is_login_page_visible(), "Login page should be visible"
        
        login_page.login(credentials["email"], credentials["password"])
        
        # Assert
        main_page = MainPage(page)
        page.wait_for_url("http://localhost:8080/**", timeout=30000)
        assert main_page.is_authenticated(), "User should be authenticated (Sign Out button visible)"
        
        # Verify JWT token
        token = page.evaluate("localStorage.getItem('id_token') || localStorage.getItem('token')")
        assert token is not None, "JWT token should exist in localStorage"


class TestSmokeAddressSuggestions:
    """Smoke tests for address suggestions (TC-ADDR-001)"""
    
    def test_smoke_address_suggestions(self, authenticated_page: Page):
        """
        SMOKE-002: Address suggestions display for partial input
        Verifies: Autocomplete API works, suggestions dropdown appears
        """
        # Arrange
        main_page = MainPage(authenticated_page)
        
        # Act
        main_page.enter_address(TestData.PARTIAL_ADDRESS)
        
        # Wait for suggestions
        try:
            main_page.wait_for_suggestions(timeout=5000)
        except Exception:
            pytest.fail("Suggestions dropdown should appear")
        
        # Assert
        suggestions = main_page.get_suggestions()
        assert len(suggestions) > 0, f"Should have suggestions for '{TestData.PARTIAL_ADDRESS}'"


class TestSmokeAddressValidation:
    """Smoke tests for address validation (TC-VAL-001)"""
    
    def test_smoke_valid_address_validation(self, authenticated_page: Page):
        """
        SMOKE-003: Valid address passes validation
        Verifies: Validation API works, returns valid result
        """
        # Arrange
        main_page = MainPage(authenticated_page)
        
        # Act
        main_page.enter_address(TestData.VALID_ADDRESS)
        main_page.click_validate()
        
        # Wait for validation result
        try:
            main_page.wait_for_validation_result(timeout=10000)
        except Exception:
            pytest.fail("Validation result should appear within 10 seconds")
        
        # Assert
        result = main_page.get_validation_result()
        assert result, "Validation result message should be displayed"
        # Result should indicate success (exact text depends on implementation)
        assert "valid" in result.lower() or "success" in result.lower() or "ok" in result.lower(), \
            f"Result should indicate valid address, got: {result}"
