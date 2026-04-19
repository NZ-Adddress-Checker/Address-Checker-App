"""Main Application Page Object"""
from playwright.sync_api import Page
from tests.pages.base_page import BasePage


class MainPage(BasePage):
    """Main application page object"""
    
    # Locators
    SIGN_OUT_BUTTON = 'button:has-text("Sign Out"), button:has-text("Logout"), button:has-text("sign out")'
    ADDRESS_INPUT = 'input[name="address"], input[id*="address"], input[placeholder*="address" i]'
    VALIDATE_BUTTON = 'button:has-text("Validate"), button:has-text("Validate Address")'
    SUGGESTIONS_DROPDOWN = '[role="listbox"], .dropdown, [class*="suggestion"]'
    SUGGESTION_ITEM = '[role="option"], .suggestion-item, [class*="suggestion-item"]'
    VALIDATION_RESULT = '[class*="result"], [class*="validation"], [role="alert"]'
    LOADING_SPINNER = '[class*="loading"], [class*="spinner"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "http://localhost:8080"
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (sign out button visible)"""
        return self.is_element_visible(self.SIGN_OUT_BUTTON)
    
    def sign_out(self):
        """Sign out user"""
        self.click_element(self.SIGN_OUT_BUTTON)
    
    def enter_address(self, address: str):
        """Enter address in search field"""
        self.fill_input(self.ADDRESS_INPUT, address)
    
    def get_address_input_value(self) -> str:
        """Get address input value"""
        return self.get_input_value(self.ADDRESS_INPUT)
    
    def click_validate(self):
        """Click validate button"""
        self.click_element(self.VALIDATE_BUTTON)
    
    def wait_for_suggestions(self, timeout: int = 5000):
        """Wait for suggestions dropdown to appear"""
        self.wait_for_element(self.SUGGESTIONS_DROPDOWN, timeout=timeout)
    
    def get_suggestions(self) -> list:
        """Get list of suggestions"""
        self.wait_for_suggestions()
        suggestions = self.page.query_selector_all(self.SUGGESTION_ITEM)
        return [s.text_content() for s in suggestions]
    
    def select_first_suggestion(self):
        """Select first suggestion from dropdown"""
        suggestions = self.page.query_selector_all(self.SUGGESTION_ITEM)
        if suggestions:
            suggestions[0].click()
    
    def is_loading_visible(self) -> bool:
        """Check if loading spinner is visible"""
        return self.is_element_visible(self.LOADING_SPINNER)
    
    def wait_for_validation_result(self, timeout: int = 10000):
        """Wait for validation result to appear"""
        self.wait_for_element(self.VALIDATION_RESULT, timeout=timeout)
    
    def get_validation_result(self) -> str:
        """Get validation result text"""
        return self.get_element_text(self.VALIDATION_RESULT)
