from pages.example_page import ExamplePage

class CommonKeywords:
    """
    Keyword-driven approach: High-level actions that combine multiple page operations.
    """
    def __init__(self, driver):
        self.driver = driver
        self.example_page = ExamplePage(driver)

    def perform_search_and_verify(self, term):
        self.example_page.open_url("https://www.google.com")
        self.example_page.search_for(term)
        return self.example_page.is_displayed(self.example_page.RESULT_STATS)
