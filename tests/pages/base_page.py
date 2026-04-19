"""Base Page Object class with stable, reusable methods"""
from playwright.sync_api import Page, TimeoutError, PlaywrightException
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects with stable, reusable methods
    Includes retry logic, robust waiting, and comprehensive error handling
    """
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8080"):
        self.page = page
        self.base_url = base_url
        self.default_timeout = 30000
    
    def navigate(self, path: str = ""):
        """Navigate to page with proper wait and error handling"""
        url = f"{self.base_url}{path}"
        try:
            logger.info(f"Navigating to {url}")
            self.page.goto(url, wait_until="networkidle")
        except TimeoutError:
            logger.warning(f"Navigation to {url} timed out, trying with 'domcontentloaded'")
            self.page.goto(url, wait_until="domcontentloaded")
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def wait_for_navigation(self, timeout: int = 30000):
        """Wait for page navigation"""
        try:
            with self.page.expect_navigation(timeout=timeout):
                pass
        except TimeoutError:
            logger.warning(f"Navigation timeout after {timeout}ms")
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible with proper error handling
        Supports multiple selector formats for flexibility
        """
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except TimeoutError:
            logger.debug(f"Element not visible: {selector}")
            return False
        except PlaywrightException:
            logger.debug(f"Invalid selector: {selector}")
            return False
    
    def wait_for_element(self, selector: str, timeout: int = 30000, state: str = "visible"):
        """
        Wait for element with state validation
        States: 'attached', 'detached', 'visible', 'hidden'
        """
        try:
            logger.debug(f"Waiting for element: {selector} (state={state})")
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
        except TimeoutError:
            logger.error(f"Timeout waiting for element: {selector}")
            raise AssertionError(f"Element not found or not {state}: {selector}")
    
    def click_element(self, selector: str, retry_count: int = 3):
        """
        Click element with retry logic for flaky interactions
        """
        for attempt in range(retry_count):
            try:
                logger.debug(f"Clicking element: {selector} (attempt {attempt + 1}/{retry_count})")
                self.wait_for_element(selector, timeout=5000, state="visible")
                self.page.click(selector, force=False)
                logger.debug(f"Successfully clicked: {selector}")
                return
            except Exception as e:
                logger.warning(f"Click attempt {attempt + 1} failed: {str(e)}")
                if attempt < retry_count - 1:
                    self.page.wait_for_timeout(500)
                else:
                    raise AssertionError(f"Failed to click element after {retry_count} attempts: {selector}")
    
    def fill_input(self, selector: str, text: str, clear_first: bool = True):
        """
        Fill input field with clear and validation
        """
        try:
            logger.debug(f"Filling input: {selector}")
            self.wait_for_element(selector, timeout=5000, state="visible")
            
            if clear_first:
                self.page.fill(selector, "")  # Clear first
            
            self.page.fill(selector, text)
            
            # Verify input was filled
            actual_value = self.get_input_value(selector)
            assert actual_value == text, f"Input value mismatch. Expected: {text}, Got: {actual_value}"
            logger.debug(f"Successfully filled input: {selector}")
        except Exception as e:
            logger.error(f"Failed to fill input {selector}: {str(e)}")
            raise
    
    def get_input_value(self, selector: str) -> str:
        """Get input field value with error handling"""
        try:
            self.wait_for_element(selector, timeout=5000, state="attached")
            value = self.page.input_value(selector)
            logger.debug(f"Input value for {selector}: {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to get input value for {selector}: {str(e)}")
            raise
    
    def get_element_text(self, selector: str) -> str:
        """Get element text with proper trimming and error handling"""
        try:
            self.wait_for_element(selector, timeout=5000, state="visible")
            text = self.page.text_content(selector)
            result = text.strip() if text else ""
            logger.debug(f"Element text for {selector}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get element text for {selector}: {str(e)}")
            raise
    
    def get_all_elements_text(self, selector: str) -> List[str]:
        """Get text from multiple elements"""
        try:
            self.wait_for_element(selector, timeout=5000, state="attached")
            elements = self.page.query_selector_all(selector)
            texts = [elem.text_content().strip() for elem in elements if elem.text_content()]
            logger.debug(f"Got {len(texts)} elements from {selector}")
            return texts
        except Exception as e:
            logger.error(f"Failed to get element texts for {selector}: {str(e)}")
            raise
    
    def wait_for_url(self, url_pattern: str, timeout: int = 30000):
        """Wait for URL to match pattern"""
        try:
            logger.debug(f"Waiting for URL: {url_pattern}")
            self.page.wait_for_url(url_pattern, timeout=timeout)
            logger.debug(f"URL matched: {url_pattern}")
        except TimeoutError:
            current_url = self.page.url
            logger.error(f"URL timeout. Expected: {url_pattern}, Got: {current_url}")
            raise
    
    def take_screenshot(self, filename: str, full_page: bool = False):
        """Take screenshot with error handling"""
        try:
            logger.info(f"Taking screenshot: {filename}")
            self.page.screenshot(path=filename, full_page=full_page)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def wait_for_timeout(self, ms: int):
        """Wait for specified time (use sparingly)"""
        logger.debug(f"Waiting {ms}ms")
        self.page.wait_for_timeout(ms)
    
    def press_key(self, key: str):
        """Press keyboard key"""
        logger.debug(f"Pressing key: {key}")
        self.page.keyboard.press(key)
    
    def keyboard_type(self, text: str):
        """Type text using keyboard"""
        logger.debug(f"Typing: {text}")
        self.page.keyboard.type(text)
    
    def get_page_title(self) -> str:
        """Get page title"""
        title = self.page.title()
        logger.debug(f"Page title: {title}")
        return title
    
    def is_element_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        try:
            element = self.page.query_selector(selector)
            return element is not None and element.is_enabled()
        except Exception:
            return False
    
    def wait_for_element_count(self, selector: str, expected_count: int, timeout: int = 10000):
        """Wait for specific number of elements"""
        import time
        start = time.time()
        
        while (time.time() - start) * 1000 < timeout:
            try:
                elements = self.page.query_selector_all(selector)
                if len(elements) == expected_count:
                    logger.debug(f"Found {expected_count} elements for {selector}")
                    return elements
                self.page.wait_for_timeout(500)
            except Exception:
                self.page.wait_for_timeout(500)
        
        raise AssertionError(f"Expected {expected_count} elements, but timeout reached")
