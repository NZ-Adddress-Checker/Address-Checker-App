from pages.base_page import BasePage

class NoAccessPage(BasePage):

    MESSAGE = "text=No access to this feature."

    def shown(self):
        # Wait for page to load and check both URL and message
        self.page.wait_for_url("**/no-access", timeout=10000)
        return self.is_visible(self.MESSAGE)