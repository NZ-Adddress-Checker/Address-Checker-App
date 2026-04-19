"""
Sanity Tests for NZ Address Checker Application
Sanity tests verify key features work after deployment
These tests are stable and reusable with comprehensive error handling
"""
import pytest
import logging
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.main_page import MainPage
from tests.utils.test_data import TestData
from tests.utils.helpers import TestHelper, StorageHelper

logger = logging.getLogger(__name__)


class TestSanityAuthentication:
    """Sanity tests for authentication workflows"""
    
    def test_sanity_invalid_login(self, page: Page):
        """
        SANITY-001: Login fails with invalid password (TC-AUTH-002)
        Verifies: Authentication validation works, invalid creds rejected
        Stability: Proper wait for error, timeout handling
        """
        logger.info("Starting SANITY-001: Invalid Login Test")
        
        # Arrange
        login_page = LoginPage(page)
        credentials = TestData.get_invalid_credentials()
        logger.debug(f"Testing invalid login for {credentials['email']}")
        
        # Act
        login_page.navigate()
        assert login_page.is_login_page_visible(), "Login page should be visible"
        
        login_page.login(credentials["email"], credentials["password"])
        logger.debug("Login attempt with invalid password completed")
        
        # Wait for error or stay on login
        page.wait_for_timeout(3000)  # Allow time for Cognito response
        
        # Assert - Check for error or login page
        current_url = page.url
        is_login_page = login_page.is_login_page_visible()
        is_error_visible = login_page.is_error_message_visible()
        
        assert is_login_page or is_error_visible or "cognito" in current_url.lower(), \
            f"Should handle invalid credentials. URL: {current_url}, Error visible: {is_error_visible}"
        
        logger.info("SANITY-001 passed: Invalid login properly rejected")
    
    def test_sanity_logout(self, authenticated_page: Page):
        """
        SANITY-002: User successfully logs out (TC-AUTH-003)
        Verifies: Logout clears session, user redirected to login
        Stability: Proper verification of logout
        """
        logger.info("Starting SANITY-002: Logout Test")
        
        # Arrange
        main_page = MainPage(authenticated_page)
        assert main_page.is_authenticated(), "User should be authenticated initially"
        logger.debug("User is authenticated")
        
        # Act
        main_page.sign_out()
        logger.debug("Clicked sign out button")
        
        # Wait for logout to complete
        authenticated_page.wait_for_timeout(2000)
        
        # Assert
        login_page = LoginPage(authenticated_page)
        assert login_page.is_login_page_visible(), "Should be redirected to login page"
        logger.debug("Login page is visible")
        
        # Verify token is cleared
        token = StorageHelper.get_jwt_token(authenticated_page)
        assert token is None, "JWT token should be cleared after logout"
        logger.debug("JWT token cleared")
        
        logger.info("SANITY-002 passed: Logout successful")


class TestSanityAddressFeatures:
    """Sanity tests for address feature workflows"""
    
    def test_sanity_select_suggestion(self, authenticated_page: Page):
        """
        SANITY-003: User can select address from suggestions (TC-ADDR-003)
        Verifies: Suggestion selection populates input field
        Stability: Proper wait for suggestions, selection validation
        """
        logger.info("Starting SANITY-003: Select Suggestion Test")
        
        # Arrange
        main_page = MainPage(authenticated_page)
        test_address = TestData.PARTIAL_ADDRESS
        logger.debug(f"Testing suggestion selection with: {test_address}")
        
        # Act - Enter address
        main_page.enter_address(test_address)
        logger.debug("Address entered")
        
        # Act - Wait for suggestions
        try:
            main_page.wait_for_suggestions(timeout=5000)
            logger.debug("Suggestions appeared")
        except AssertionError as e:
            logger.error(f"Suggestions failed to appear: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/sanity_003_suggestions_failed.png")
            raise
        
        # Act - Select first suggestion
        main_page.select_first_suggestion()
        logger.debug("Selected first suggestion")
        
        # Wait for selection to populate
        authenticated_page.wait_for_timeout(1000)
        
        # Assert
        selected_address = main_page.get_address_input_value()
        TestHelper.assert_not_empty(selected_address, "Address input should be populated after selection")
        logger.info(f"SANITY-003 passed: Selected address - {selected_address}")
    
    def test_sanity_invalid_address_validation(self, authenticated_page: Page):
        """
        SANITY-004: Invalid address fails validation (TC-VAL-002)
        Verifies: Validation correctly rejects invalid addresses
        Stability: Result assertion with multiple indicators
        """
        logger.info("Starting SANITY-004: Invalid Address Validation Test")
        
        # Arrange
        main_page = MainPage(authenticated_page)
        test_address = TestData.INVALID_ADDRESS
        logger.debug(f"Testing validation with invalid address: {test_address}")
        
        # Act - Enter address
        main_page.enter_address(test_address)
        logger.debug("Invalid address entered")
        
        # Act - Click validate
        main_page.click_validate()
        logger.debug("Clicked validate")
        
        # Act - Wait for result
        try:
            main_page.wait_for_validation_result(timeout=10000)
            logger.debug("Validation result appeared")
        except AssertionError as e:
            logger.error(f"Validation result timeout: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/sanity_004_timeout.png")
            raise
        
        # Assert - Get result
        try:
            result = main_page.get_validation_result()
            TestHelper.assert_not_empty(result, "Validation result should be displayed")
            logger.debug(f"Validation result: {result}")
            
            # Check for failure indicators
            result_lower = result.lower()
            assert any(indicator in result_lower for indicator in ["invalid", "not found", "error", "failed", "incorrect"]), \
                f"Result should indicate invalid address, got: {result}"
            
            logger.info(f"SANITY-004 passed: Invalid address rejected - {result}")
        except AssertionError as e:
            logger.error(f"Result assertion failed: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/sanity_004_result.png")
            raise


class TestSanityEndToEndWorkflow:
    """Sanity tests for complete user workflows"""
    
    def test_sanity_complete_address_workflow(self, authenticated_page: Page):
        """
        SANITY-005: Complete login → suggest → validate → logout (TC-JRN-001)
        Verifies: All major features work together
        Stability: Step-by-step verification with proper error handling
        """
        logger.info("Starting SANITY-005: Complete Address Workflow Test")
        
        # Arrange
        main_page = MainPage(authenticated_page)
        assert main_page.is_authenticated(), "User should be logged in"
        logger.debug("Step 1: User is authenticated")
        
        # Step 2: Address suggestion
        test_address = TestData.PARTIAL_ADDRESS
        main_page.enter_address(test_address)
        logger.debug(f"Step 2: Entered address: {test_address}")
        
        try:
            main_page.wait_for_suggestions(timeout=5000)
            suggestions = main_page.get_suggestions()
            assert len(suggestions) > 0, "Should have suggestions"
            logger.debug(f"Step 2: Got {len(suggestions)} suggestions")
        except AssertionError as e:
            logger.error(f"Suggestions failed at step 2: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/sanity_005_step2.png")
            raise
        
        # Step 3: Select suggestion
        main_page.select_first_suggestion()
        authenticated_page.wait_for_timeout(1000)
        selected = main_page.get_address_input_value()
        TestHelper.assert_not_empty(selected, "Should have selected an address")
        logger.debug(f"Step 3: Selected address: {selected}")
        
        # Step 4: Validate address
        main_page.click_validate()
        logger.debug("Step 4: Clicked validate")
        
        try:
            main_page.wait_for_validation_result(timeout=10000)
            result = main_page.get_validation_result()
            TestHelper.assert_not_empty(result, "Should display validation result")
            logger.debug(f"Step 4: Validation result: {result}")
        except AssertionError as e:
            logger.error(f"Validation failed at step 4: {str(e)}")
            authenticated_page.screenshot(path="tests/screenshots/sanity_005_step4.png")
            raise
        
        # Step 5: Logout
        main_page.sign_out()
        authenticated_page.wait_for_timeout(2000)
        logger.debug("Step 5: Clicked sign out")
        
        login_page = LoginPage(authenticated_page)
        assert login_page.is_login_page_visible(), "Should be back on login page"
        logger.debug("Step 5: Back on login page")
        
        logger.info("SANITY-005 passed: Complete workflow successful")

