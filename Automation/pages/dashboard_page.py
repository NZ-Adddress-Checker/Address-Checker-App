from pages.base_page import BasePage

class DashboardPage(BasePage):

    ADDRESS_INPUT = "input.address-input"
    DROPDOWN_ITEM = ".suggestion-item"
    VALIDATE_BUTTON = "text=Validate"
    VALID_TEXT = "text=Valid: Yes ✓"
    ERROR_MESSAGE = ".error-message"
    LOGOUT = "text=Logout"

    def search_address(self, text):
        self.fill(self.ADDRESS_INPUT, text)
        self.wait(1000)  # Wait for debounce (300ms) + API response

    def select_first(self):
        self.page.wait_for_selector(self.DROPDOWN_ITEM, timeout=10000)
        self.click(self.DROPDOWN_ITEM)

    def validate(self):
        self.click(self.VALIDATE_BUTTON)
        self.wait(1000)  # Wait for validation response

    def is_valid(self):
        return self.is_visible(self.VALID_TEXT)

    def has_error(self, message=None):
        """Check if error message is shown. Optionally check for specific message text."""
        if message:
            return self.is_visible(f"text={message}")
        return self.is_visible(self.ERROR_MESSAGE)

    def logout(self):
        self.click(self.LOGOUT)