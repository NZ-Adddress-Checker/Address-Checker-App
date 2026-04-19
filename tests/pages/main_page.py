"""Main Application Page Object with stable, reusable methods"""
from playwright.sync_api import Page, TimeoutError
from tests.pages.base_page import BasePage
from typing import List
import logging

logger = logging.getLogger(__name__)


class MainPage(BasePage):
    """
    Main application page object with multiple selector strategies
    Handles different UI variations for stability and reusability
    """
    
    # Multiple selector strategies
    SIGN_OUT_SELECTORS = [
        'button:has-text("Sign Out")',
        'button:has-text("Logout")',
        'button:has-text("logout")',
        'a:has-text("Sign Out")',
    ]
    
    ADDRESS_INPUT_SELECTORS = [
        'input[name="address"]',
        'input[id*="address"]',
        'input[placeholder*="address" i]',
        '[data-testid="address-input"]',
    ]
    
    VALIDATE_BUTTON_SELECTORS = [
        'button:has-text("Validate")',
        'button:has-text("Validate Address")',
        'button:has-text("Check")',
        '[data-testid="validate-button"]',
    ]
    
    SUGGESTIONS_SELECTORS = [
        '[role="listbox"]',
        '.dropdown',
        '[class*="suggestion"]',
        '[class*="autocomplete"]',
    ]
    
    SUGGESTION_ITEM_SELECTORS = [
        '[role="option"]',
        '.suggestion-item',
        '[class*="suggestion-item"]',
        '.dropdown-item',
    ]
    
    VALIDATION_RESULT_SELECTORS = [
        '[class*="result"]',
        '[class*="validation"]',
        '[role="alert"]',
        '[class*="message"]',
    ]
    
    LOADING_SPINNER_SELECTORS = [
        '[class*="loading"]',
        '[class*="spinner"]',
        '[aria-busy="true"]',
    ]
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "http://localhost:8080"
    
    def _find_element(self, selectors: List[str], timeout: int = 5000):
        """Try multiple selectors and return the first visible one"""
        for selector in selectors:
            try:
                if self.is_element_visible(selector, timeout=timeout):
                    logger.debug(f"Found element with selector: {selector}")
                    return selector
            except Exception:
                continue
        
        raise AssertionError(f"Element not found with any of {len(selectors)} selectors")
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (sign out button visible)"""
        logger.debug("Checking authentication status")
        try:
            sign_out_selector = self._find_element(self.SIGN_OUT_SELECTORS, timeout=3000)
            logger.info("User is authenticated")
            return True
        except AssertionError:
            logger.info("User is not authenticated")
            return False
    
    def sign_out(self):
        """Sign out user"""
        logger.info("Signing out user")
        try:
            sign_out_selector = self._find_element(self.SIGN_OUT_SELECTORS)
            self.click_element(sign_out_selector, retry_count=3)
            logger.info("Sign out completed")
        except Exception as e:
            logger.error(f"Failed to sign out: {str(e)}")
            raise
    
    def enter_address(self, address: str):
        """Enter address in search field"""
        logger.info(f"Entering address: {address}")
        try:
            address_selector = self._find_element(self.ADDRESS_INPUT_SELECTORS)
            self.fill_input(address_selector, address)
        except Exception as e:
            logger.error(f"Failed to enter address: {str(e)}")
            raise
    
    def get_address_input_value(self) -> str:
        """Get address input value"""
        logger.debug("Getting address input value")
        try:
            address_selector = self._find_element(self.ADDRESS_INPUT_SELECTORS, timeout=3000)
            return self.get_input_value(address_selector)
        except Exception as e:
            logger.error(f"Failed to get address value: {str(e)}")
            raise
    
    def click_validate(self):
        """Click validate button"""
        logger.info("Clicking validate button")
        try:
            validate_selector = self._find_element(self.VALIDATE_BUTTON_SELECTORS)
            self.click_element(validate_selector, retry_count=3)
        except Exception as e:
            logger.error(f"Failed to click validate: {str(e)}")
            raise
    
    def wait_for_suggestions(self, timeout: int = 5000):
        """Wait for suggestions dropdown to appear"""
        logger.info("Waiting for suggestions")
        try:
            suggestions_selector = self._find_element(self.SUGGESTIONS_SELECTORS, timeout=timeout)
            logger.info("Suggestions appeared")
        except AssertionError:
            logger.error("Suggestions did not appear")
            raise
    
    def get_suggestions(self) -> List[str]:
        """Get list of suggestions"""
        logger.info("Getting suggestions list")
        try:
            self.wait_for_suggestions()
            
            # Try to find suggestion items
            suggestions = []
            for selector in self.SUGGESTION_ITEM_SELECTORS:
                try:
                    items = self.get_all_elements_text(selector)
                    if items:
                        suggestions = items
                        break
                except Exception:
                    continue
            
            logger.info(f"Found {len(suggestions)} suggestions")
            return suggestions
        except Exception as e:
            logger.error(f"Failed to get suggestions: {str(e)}")
            raise
    
    def select_first_suggestion(self):
        """Select first suggestion from dropdown"""
        logger.info("Selecting first suggestion")
        try:
            # Find first suggestion item
            for selector in self.SUGGESTION_ITEM_SELECTORS:
                try:
                    elements = self.page.query_selector_all(selector)
                    if elements:
                        elements[0].click()
                        logger.info("First suggestion selected")
                        return
                except Exception:
                    continue
            
            raise AssertionError("No suggestion items found to select")
        except Exception as e:
            logger.error(f"Failed to select suggestion: {str(e)}")
            raise
    
    def is_loading_visible(self) -> bool:
        """Check if loading spinner is visible"""
        logger.debug("Checking loading state")
        for selector in self.LOADING_SPINNER_SELECTORS:
            if self.is_element_visible(selector, timeout=2000):
                logger.debug("Loading spinner visible")
                return True
        return False
    
    def wait_for_validation_result(self, timeout: int = 10000):
        """Wait for validation result to appear"""
        logger.info("Waiting for validation result")
        try:
            result_selector = self._find_element(self.VALIDATION_RESULT_SELECTORS, timeout=timeout)
            # Wait for loading to finish first
            self.page.wait_for_timeout(500)  # Brief pause
            # Wait for element to be visible
            self.wait_for_element(result_selector, timeout=timeout, state="visible")
            logger.info("Validation result appeared")
        except AssertionError as e:
            logger.error(f"Validation result not found: {str(e)}")
            raise
    
    def get_validation_result(self) -> str:
        """Get validation result text"""
        logger.info("Getting validation result")
        try:
            # Try to find result with any selector
            for selector in self.VALIDATION_RESULT_SELECTORS:
                try:
                    if self.is_element_visible(selector, timeout=2000):
                        return self.get_element_text(selector)
                except Exception:
                    continue
            
            raise AssertionError("Validation result not found")
        except Exception as e:
            logger.error(f"Failed to get validation result: {str(e)}")
            raise
    
    def clear_address_input(self):
        """Clear address input field"""
        logger.info("Clearing address input")
        try:
            address_selector = self._find_element(self.ADDRESS_INPUT_SELECTORS)
            self.page.fill(address_selector, "")
            logger.info("Address input cleared")
        except Exception as e:
            logger.error(f"Failed to clear address: {str(e)}")
            raise
    
    def wait_for_loading_complete(self, timeout: int = 10000):
        """Wait for loading spinner to disappear"""
        logger.info("Waiting for loading to complete")
        import time
        start = time.time()
        
        while (time.time() - start) * 1000 < timeout:
            if not self.is_loading_visible():
                logger.info("Loading complete")
                return
            self.page.wait_for_timeout(500)
        
        logger.warning("Loading timeout reached")
        raise TimeoutError("Loading did not complete within timeout")
