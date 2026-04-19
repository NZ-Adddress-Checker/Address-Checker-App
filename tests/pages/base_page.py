"""Base Page Object class for all pages"""
from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        self.page = page
        self.base_url = base_url
    
    def navigate(self, path: str = ""):
        """Navigate to page"""
        url = f"{self.base_url}{path}"
        self.page.goto(url)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def wait_for_navigation(self, timeout: int = 30000):
        """Wait for page navigation"""
        with self.page.expect_navigation():
            pass
    
    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            element = self.page.query_selector(selector)
            return element is not None and element.is_visible()
        except Exception:
            return False
    
    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Wait for element to be visible"""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def click_element(self, selector: str):
        """Click element by selector"""
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str):
        """Fill input field"""
        self.page.fill(selector, text)
    
    def get_input_value(self, selector: str) -> str:
        """Get input field value"""
        return self.page.input_value(selector)
    
    def get_element_text(self, selector: str) -> str:
        """Get element text"""
        return self.page.text_content(selector)
    
    def wait_for_url(self, url_pattern: str, timeout: int = 30000):
        """Wait for URL to match pattern"""
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def take_screenshot(self, filename: str):
        """Take screenshot"""
        self.page.screenshot(path=filename)
