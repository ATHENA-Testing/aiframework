from selenium.webdriver.remote.webdriver import WebDriver
from base.waits import WaitUtils
from utils.logger import logger

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtils(driver)

    def open_url(self, url):
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.wait_for_element_visible(locator)

    def click(self, locator):
        logger.info(f"Clicking on element: {locator}")
        self.find_element(locator).click()

    def enter_text(self, locator, text):
        logger.info(f"Entering text '{text}' into element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        text = self.find_element(locator).text
        logger.info(f"Text found: {text}")
        return text

    def is_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def take_screenshot(self, name):
        import os
        if not os.path.exists("reports/screenshots"):
            os.makedirs("reports/screenshots")
        path = f"reports/screenshots/{name}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved to {path}")
