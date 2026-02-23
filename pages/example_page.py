from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base.base_page import BasePage

class ExamplePage(BasePage):
    # Locators
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    RESULT_STATS = (By.ID, "result-stats")

    def __init__(self, driver):
        super().__init__(driver)

    def search_for(self, term):
        self.enter_text(self.SEARCH_BOX, term)
        # Use the new press_key method from BasePage
        self.press_key(self.SEARCH_BOX, Keys.RETURN)

    def get_results_text(self):
        return self.get_text(self.RESULT_STATS)
