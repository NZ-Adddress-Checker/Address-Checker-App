"""Login Page Object"""
from playwright.sync_api import Page
from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    EMAIL_INPUT = 'input[name="email"], input[id*="email"], input[placeholder*="email" i]'
    PASSWORD_INPUT = 'input[name="password"], input[id*="password"], input[placeholder*="password" i]'
    SIGN_IN_BUTTON = 'button:has-text("Sign In"), button:has-text("Login"), button:has-text("sign in")'
    ERROR_MESSAGE = '.error, [class*="error"], [role="alert"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "http://localhost:8080"
    
    def navigate(self):
        """Navigate to login page"""
        super().navigate("/")
    
    def enter_email(self, email: str):
        """Enter email address"""
        self.fill_input(self.EMAIL_INPUT, email)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.fill_input(self.PASSWORD_INPUT, password)
    
    def click_sign_in(self):
        """Click sign in button"""
        self.click_element(self.SIGN_IN_BUTTON)
    
    def login(self, email: str, password: str):
        """Perform login"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in()
    
    def is_login_page_visible(self) -> bool:
        """Check if login page is visible"""
        return self.is_element_visible(self.SIGN_IN_BUTTON)
    
    def is_error_message_visible(self) -> bool:
        """Check if error message is visible"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        try:
            return self.get_element_text(self.ERROR_MESSAGE)
        except:
            return ""
