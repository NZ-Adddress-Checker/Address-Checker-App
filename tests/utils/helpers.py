"""Test helpers and utilities for reusable test code"""
import logging
from typing import Callable, Any
from playwright.sync_api import Page, TimeoutError

logger = logging.getLogger(__name__)


class TestHelper:
    """Helper class with common test operations"""
    
    @staticmethod
    def retry_action(action: Callable, max_retries: int = 3, wait_ms: int = 500, description: str = "Action"):
        """
        Retry an action multiple times until it succeeds
        
        Args:
            action: Callable to execute
            max_retries: Maximum number of retry attempts
            wait_ms: Wait time between retries in milliseconds
            description: Description of the action for logging
        
        Returns:
            Result of the action
        
        Raises:
            Exception: If action fails after all retries
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"{description} - Attempt {attempt + 1}/{max_retries}")
                result = action()
                logger.debug(f"{description} - Success on attempt {attempt + 1}")
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"{description} - Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    # Wait before retry
                    import time
                    time.sleep(wait_ms / 1000)
        
        raise AssertionError(f"{description} failed after {max_retries} attempts: {str(last_error)}")
    
    @staticmethod
    def wait_for_condition(condition: Callable[[], bool], timeout_ms: int = 10000, 
                          check_interval_ms: int = 500, description: str = "Condition"):
        """
        Wait for a condition to become true
        
        Args:
            condition: Callable that returns boolean
            timeout_ms: Maximum wait time in milliseconds
            check_interval_ms: Interval between checks in milliseconds
            description: Description for logging
        
        Raises:
            TimeoutError: If condition not met within timeout
        """
        import time
        start = time.time()
        
        while (time.time() - start) * 1000 < timeout_ms:
            try:
                if condition():
                    logger.debug(f"{description} - Condition met")
                    return
                time.sleep(check_interval_ms / 1000)
            except Exception as e:
                logger.debug(f"{description} - Check failed: {str(e)}")
                time.sleep(check_interval_ms / 1000)
        
        logger.error(f"{description} - Timeout after {timeout_ms}ms")
        raise TimeoutError(f"{description} timeout after {timeout_ms}ms")
    
    @staticmethod
    def assert_equals(actual: Any, expected: Any, message: str = ""):
        """
        Assert equality with detailed error message
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom error message
        
        Raises:
            AssertionError: If values don't match
        """
        if actual != expected:
            error_msg = f"Expected: '{expected}', Got: '{actual}'"
            if message:
                error_msg = f"{message}\n{error_msg}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Assertion passed: {expected}")
    
    @staticmethod
    def assert_contains(text: str, substring: str, message: str = ""):
        """
        Assert that text contains substring
        
        Args:
            text: Text to search in
            substring: Substring to search for
            message: Custom error message
        
        Raises:
            AssertionError: If substring not found
        """
        if substring not in text:
            error_msg = f"'{text}' does not contain '{substring}'"
            if message:
                error_msg = f"{message}\n{error_msg}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Text contains substring: {substring}")
    
    @staticmethod
    def assert_not_empty(value: str, message: str = ""):
        """
        Assert that value is not empty
        
        Args:
            value: Value to check
            message: Custom error message
        
        Raises:
            AssertionError: If value is empty
        """
        if not value or not value.strip():
            error_msg = f"Expected non-empty value, got: '{value}'"
            if message:
                error_msg = f"{message}\n{error_msg}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Value is not empty: {value}")


class FormHelper:
    """Helper class for form interactions"""
    
    @staticmethod
    def fill_form_field(page: Page, selector: str, value: str, clear_first: bool = True):
        """
        Fill a form field with validation
        
        Args:
            page: Playwright page object
            selector: Element selector
            value: Value to fill
            clear_first: Clear field before filling
        """
        logger.debug(f"Filling field: {selector} with value: {value}")
        try:
            page.wait_for_selector(selector, state="visible", timeout=5000)
            if clear_first:
                page.fill(selector, "")
            page.fill(selector, value)
            
            # Verify
            actual = page.input_value(selector)
            TestHelper.assert_equals(actual, value, f"Form field value mismatch")
        except Exception as e:
            logger.error(f"Failed to fill form field: {str(e)}")
            raise
    
    @staticmethod
    def submit_form(page: Page, submit_selector: str):
        """
        Submit form with validation
        
        Args:
            page: Playwright page object
            submit_selector: Submit button selector
        """
        logger.debug(f"Submitting form with: {submit_selector}")
        try:
            page.wait_for_selector(submit_selector, state="visible", timeout=5000)
            page.click(submit_selector)
            logger.debug("Form submitted")
        except Exception as e:
            logger.error(f"Failed to submit form: {str(e)}")
            raise


class NavigationHelper:
    """Helper class for navigation operations"""
    
    @staticmethod
    def navigate_and_wait(page: Page, url: str, wait_until: str = "networkidle", timeout: int = 30000):
        """
        Navigate to URL and wait for page load
        
        Args:
            page: Playwright page object
            url: URL to navigate to
            wait_until: 'load', 'domcontentloaded', or 'networkidle'
            timeout: Navigation timeout
        """
        logger.info(f"Navigating to: {url}")
        try:
            page.goto(url, wait_until=wait_until, timeout=timeout)
            logger.info(f"Navigation complete: {page.url}")
        except TimeoutError:
            logger.warning(f"Navigation timeout, trying with {wait_until}")
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
    
    @staticmethod
    def get_page_title(page: Page) -> str:
        """Get page title"""
        title = page.title()
        logger.debug(f"Page title: {title}")
        return title
    
    @staticmethod
    def is_on_page(page: Page, url_pattern: str) -> bool:
        """Check if on expected page"""
        import re
        is_on = re.match(url_pattern, page.url) is not None
        logger.debug(f"On page {url_pattern}: {is_on}")
        return is_on


class StorageHelper:
    """Helper class for storage operations"""
    
    @staticmethod
    def get_local_storage(page: Page, key: str) -> str:
        """Get value from localStorage"""
        logger.debug(f"Getting localStorage: {key}")
        return page.evaluate(f"localStorage.getItem('{key}')")
    
    @staticmethod
    def set_local_storage(page: Page, key: str, value: str):
        """Set value in localStorage"""
        logger.debug(f"Setting localStorage: {key}")
        page.evaluate(f"localStorage.setItem('{key}', '{value}')")
    
    @staticmethod
    def clear_storage(page: Page):
        """Clear all storage"""
        logger.debug("Clearing storage")
        page.evaluate("localStorage.clear();sessionStorage.clear();")
    
    @staticmethod
    def get_jwt_token(page: Page) -> str:
        """Get JWT token from storage"""
        token = page.evaluate(
            "localStorage.getItem('id_token') || localStorage.getItem('token') || localStorage.getItem('jwt')"
        )
        logger.debug(f"JWT token {'found' if token else 'not found'}")
        return token
