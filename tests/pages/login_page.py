"""Login Page Object with stable, reusable methods"""
from playwright.sync_api import Page, TimeoutError
from tests.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Login page object with multiple selector strategies for stability
    Handles different UI variations and provides comprehensive assertions
    """
    
    # Multiple selector strategies for robustness
    EMAIL_SELECTORS = [
        'input[name="email"]',
        'input[id*="email"]',
        'input[placeholder*="email" i]',
        'input[type="email"]',
    ]
    
    PASSWORD_SELECTORS = [
        'input[name="password"]',
        'input[id*="password"]',
        'input[placeholder*="password" i]',
        'input[type="password"]',
    ]
    
    SIGN_IN_SELECTORS = [
        'button:has-text("Sign In")',
        'button:has-text("Login")',
        'button:has-text("login")',
        'button[type="submit"]',
    ]
    
    ERROR_MESSAGE_SELECTORS = [
        '.error',
        '[class*="error"]',
        '[role="alert"]',
        '[class*="alert"]',
    ]
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "http://localhost:8080"
    
    def navigate(self):
        """Navigate to login page"""
        logger.info("Navigating to login page")
        super().navigate("/")
    
    def _find_element(self, selectors: list, timeout: int = 5000):
        """Try multiple selectors and return the first visible one"""
        for selector in selectors:
            try:
                if self.is_element_visible(selector, timeout=timeout):
                    logger.debug(f"Found element with selector: {selector}")
                    return selector
            except Exception:
                continue
        
        raise AssertionError(f"Element not found with any of {len(selectors)} selectors")
    
    def enter_email(self, email: str):
        """Enter email with stable selector strategy"""
        logger.info(f"Entering email: {email}")
        try:
            email_selector = self._find_element(self.EMAIL_SELECTORS)
            self.fill_input(email_selector, email)
        except Exception as e:
            logger.error(f"Failed to enter email: {str(e)}")
            raise
    
    def enter_password(self, password: str):
        """Enter password with stable selector strategy"""
        logger.info("Entering password")
        try:
            password_selector = self._find_element(self.PASSWORD_SELECTORS)
            self.fill_input(password_selector, password)
        except Exception as e:
            logger.error(f"Failed to enter password: {str(e)}")
            raise
    
    def click_sign_in(self):
        """Click sign in button with stable selector strategy"""
        logger.info("Clicking sign in button")
        try:
            sign_in_selector = self._find_element(self.SIGN_IN_SELECTORS)
            self.click_element(sign_in_selector, retry_count=3)
        except Exception as e:
            logger.error(f"Failed to click sign in: {str(e)}")
            raise
    
    def login(self, email: str, password: str, wait_for_redirect: bool = True):
        """
        Perform complete login flow
        
        Args:
            email: User email
            password: User password
            wait_for_redirect: Wait for redirect after login
        """
        logger.info(f"Performing login for {email}")
        try:
            self.enter_email(email)
            self.enter_password(password)
            self.click_sign_in()
            
            if wait_for_redirect:
                try:
                    # Wait for redirect (could go to various pages after login)
                    self.page.wait_for_url(f"{self.base_url}/**", timeout=30000, wait_until="networkidle")
                    logger.info("Login redirect complete")
                except TimeoutError:
                    logger.warning("Login redirect timeout, trying with domcontentloaded")
                    self.page.wait_for_url(f"{self.base_url}/**", timeout=30000, wait_until="domcontentloaded")
            
            logger.info("Login completed successfully")
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise
    
    def is_login_page_visible(self) -> bool:
        """Check if login page is visible"""
        try:
            return self.is_element_visible(self.SIGN_IN_SELECTORS[0], timeout=3000)
        except Exception:
            return False
    
    def is_error_message_visible(self) -> bool:
        """Check if error message is displayed"""
        logger.debug("Checking for error message")
        for selector in self.ERROR_MESSAGE_SELECTORS:
            if self.is_element_visible(selector, timeout=2000):
                logger.debug(f"Error message found with selector: {selector}")
                return True
        return False
    
    def get_error_message(self) -> str:
        """Get error message text"""
        logger.info("Getting error message")
        try:
            for selector in self.ERROR_MESSAGE_SELECTORS:
                if self.is_element_visible(selector, timeout=2000):
                    return self.get_element_text(selector)
            return ""
        except Exception as e:
            logger.warning(f"Failed to get error message: {str(e)}")
            return ""
    
    def get_page_load_time(self) -> float:
        """Get page load time (for performance testing)"""
        return self.page.evaluate("window.performance.timing.loadEventEnd - window.performance.timing.navigationStart")
