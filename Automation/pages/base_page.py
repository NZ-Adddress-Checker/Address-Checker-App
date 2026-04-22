class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, value):
        self.page.fill(selector, value)

    def is_visible(self, selector):
        return self.page.is_visible(selector)

    def wait(self, ms=1000):
        self.page.wait_for_timeout(ms)