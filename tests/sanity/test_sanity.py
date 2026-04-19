"""
Sanity Tests for NZ Address Checker Application
Sanity tests verify key features work after deployment
"""
import pytest
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage
from tests.utils.test_data import TestData


class TestSanityAuthentication:
    """Sanity tests for authentication workflows"""
    
    def test_sanity_invalid_login(self, page: Page):
        """
        SANITY-001: Login fails with invalid password (TC-AUTH-002)
        Verifies: Authentication validation works, invalid creds rejected
        """
        # Arrange
        login_page = LoginPage(page)
        credentials = TestData.get_invalid_credentials()
        
        # Act
        login_page.navigate()
        login_page.login(credentials["email"], credentials["password"])
        
        # Wait for error or redirect
        page.wait_for_timeout(3000)  # Allow time for Cognito response
        
        # Assert - should either stay on login page or show error
        current_url = page.url
        # Check if still on login or if redirected to Cognito error
        assert "login" in current_url.lower() or "cognito" in current_url.lower() or login_page.is_error_message_visible(), \
            f"Should handle invalid credentials, current URL: {current_url}"
    
    def test_sanity_logout(self, authenticated_page: Page):
        """
        SANITY-002: User successfully logs out (TC-AUTH-003)
        Verifies: Logout clears session, user redirected to login
        """
        # Arrange
        main_page = MainPage(authenticated_page)
        assert main_page.is_authenticated(), "User should be authenticated initially"
        
        # Act
        main_page.sign_out()
        
        # Wait for redirect
        authenticated_page.wait_for_timeout(2000)
        
        # Assert
        login_page = LoginPage(authenticated_page)
        assert login_page.is_login_page_visible(), "Should be redirected to login page"
        
        # Verify token is cleared
        token = authenticated_page.evaluate("localStorage.getItem('id_token') || localStorage.getItem('token')")
        assert token is None, "JWT token should be cleared after logout"


class TestSanityAddressFeatures:
    """Sanity tests for address feature workflows"""
    
    def test_sanity_select_suggestion(self, authenticated_page: Page):
        """
        SANITY-003: User can select address from suggestions (TC-ADDR-003)
        Verifies: Suggestion selection populates input field
        """
        # Arrange
        main_page = MainPage(authenticated_page)
        
        # Act
        main_page.enter_address(TestData.PARTIAL_ADDRESS)
        main_page.wait_for_suggestions(timeout=5000)
        main_page.select_first_suggestion()
        
        # Wait for selection to populate
        authenticated_page.wait_for_timeout(1000)
        
        # Assert
        selected_address = main_page.get_address_input_value()
        assert selected_address, "Address input should be populated after selection"
        assert selected_address.strip() != "", "Selected address should not be empty"
    
    def test_sanity_invalid_address_validation(self, authenticated_page: Page):
        """
        SANITY-004: Invalid address fails validation (TC-VAL-002)
        Verifies: Validation correctly rejects invalid addresses
        """
        # Arrange
        main_page = MainPage(authenticated_page)
        
        # Act
        main_page.enter_address(TestData.INVALID_ADDRESS)
        main_page.click_validate()
        
        # Wait for result
        try:
            main_page.wait_for_validation_result(timeout=10000)
        except Exception:
            pytest.fail("Validation result should appear")
        
        # Assert
        result = main_page.get_validation_result()
        assert result, "Validation result message should be displayed"
        # Result should indicate invalid address
        assert "invalid" in result.lower() or "not found" in result.lower() or "error" in result.lower(), \
            f"Result should indicate invalid address, got: {result}"


class TestSanityEndToEndWorkflow:
    """Sanity tests for complete user workflows"""
    
    def test_sanity_complete_address_workflow(self, authenticated_page: Page):
        """
        SANITY-005: Complete login → suggest → validate → logout (TC-JRN-001)
        Verifies: All major features work together
        """
        # Arrange
        main_page = MainPage(authenticated_page)
        assert main_page.is_authenticated(), "User should be logged in"
        
        # Act & Assert - Address suggestion
        main_page.enter_address(TestData.PARTIAL_ADDRESS)
        main_page.wait_for_suggestions(timeout=5000)
        suggestions = main_page.get_suggestions()
        assert len(suggestions) > 0, "Should have address suggestions"
        
        # Act & Assert - Select suggestion
        main_page.select_first_suggestion()
        authenticated_page.wait_for_timeout(1000)
        selected = main_page.get_address_input_value()
        assert selected, "Should have selected an address"
        
        # Act & Assert - Validate address
        main_page.click_validate()
        try:
            main_page.wait_for_validation_result(timeout=10000)
        except Exception:
            pytest.fail("Should get validation result")
        
        result = main_page.get_validation_result()
        assert result, "Should display validation result"
        
        # Act & Assert - Logout
        main_page.sign_out()
        authenticated_page.wait_for_timeout(2000)
        
        login_page = LoginPage(authenticated_page)
        assert login_page.is_login_page_visible(), "Should be back on login page after logout"
