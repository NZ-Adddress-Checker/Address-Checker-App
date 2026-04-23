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
        """Login via Cognito's hosted UI.
        Clicking Start triggers a two-hop redirect:
          1. window.location → Cognito logout URL
          2. Cognito redirects back to logoutUri (localhost:5002/)
          3. useEffect sees autostart=1, calls signinRedirect → Cognito login page
        """
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.page.wait_for_selector(self.START, state="visible", timeout=10000)
        expect(self.page.locator(self.START)).to_be_visible()
        expect(self.page.locator(self.START)).to_be_enabled()
        self.wait(1500)

        # Click Start and wait for the full sequence to settle on Cognito login
        self.page.click(self.START, timeout=5000)

        # Wait directly for the Cognito username field.
        # This handles all redirect hops (Start → Cognito logout → localhost →
        # signinRedirect → Cognito login) without depending on URL pattern matching
        # or the `load` event, both of which are unreliable in CI for hosted-UI pages.
        self.page.wait_for_selector(self.USERNAME, timeout=35000)
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