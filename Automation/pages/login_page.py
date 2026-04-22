import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from config import BASE_URL


class LoginPage(BasePage):

    START = "text=Start"
    USERNAME = "input[name='username']"
    PASSWORD = "input[name='password']"
    SUBMIT = "button[type='submit']"

    def login(self, user, pwd):
        """Login via Cognito's two-step hosted UI (username -> Next -> password)."""
        # Wait for page to be fully loaded (networkidle ensures React has initialized)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        
        # Wait for Start button to be visible and enabled (actionable)
        # This ensures the button is not just in DOM, but actually clickable
        self.page.wait_for_selector(self.START, state="visible", timeout=10000)
        
        # Ensure button is actionable (not covered by other elements, fully rendered)
        expect(self.page.locator(self.START)).to_be_visible()
        expect(self.page.locator(self.START)).to_be_enabled()
        
        # Extra wait for React event handlers to attach
        self.wait(1500)
        
        # Click Start with retry logic until we successfully navigate to Cognito
        # Sometimes react-oidc-context has a race condition where the click navigates to itself
        max_retries = 5
        cognito_reached = False
        
        for attempt in range(max_retries):
            try:
                # Click Start and wait for navigation
                with self.page.expect_navigation(timeout=10000):
                    self.page.click(self.START, timeout=5000)
                
                # Verify we actually navigated to Cognito, not back to localhost
                current_url = self.page.url
                if "cognito" in current_url.lower():
                    cognito_reached = True
                    break
                else:
                    # Navigation happened but we're still on localhost - retry needed
                    print(f"Attempt {attempt + 1}: Navigated to {current_url}, retrying...")
                    if attempt < max_retries - 1:
                        # Go back to home to retry
                        self.page.goto(BASE_URL, wait_until="networkidle", timeout=10000)
                        self.page.wait_for_selector(self.START, state="visible", timeout=10000)
                        self.wait(1500)
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    # Wait before retry
                    print(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                    self.wait(1000)
                else:
                    # Final attempt failed, raise the exception
                    raise Exception(f"Failed to navigate to Cognito after {max_retries} attempts: {str(e)}")
        
        if not cognito_reached:
            raise Exception(f"Failed to reach Cognito login page after {max_retries} attempts")
        
        # Wait for the username field to appear (should be quick since we're already on Cognito)
        self.page.wait_for_selector(self.USERNAME, timeout=15000)
        # Step 1: username
        self.fill(self.USERNAME, user)
        self.click(self.SUBMIT)
        # Step 2: password
        self.page.wait_for_selector(self.PASSWORD, timeout=10000)
        self.fill(self.PASSWORD, pwd)
        # Submit password and wait for callback redirect
        with self.page.expect_navigation(timeout=30000):
            self.click(self.SUBMIT)
        # Wait for final redirect to complete (to /dashboard or /no-access)
        self.wait(2000)