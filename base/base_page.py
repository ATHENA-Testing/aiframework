from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from base.waits import WaitUtils
from utils.logger import logger
import os
import time

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtils(driver)
        self.actions = ActionChains(driver)

    def open_url(self, url):
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find_element(self, locator):
        """Find element using WaitUtils."""
        return self.wait.wait_for_element_visible(locator)

    def find_elements(self, locator):
        """Find multiple elements."""
        return self.driver.find_elements(*locator)

    # --- Click Actions ---
    def click(self, locator):
        logger.info(f"Clicking on element: {locator}")
        self.find_element(locator).click()

    def double_click(self, locator):
        logger.info(f"Double clicking on element: {locator}")
        element = self.find_element(locator)
        self.actions.double_click(element).perform()

    def right_click(self, locator):
        logger.info(f"Right clicking on element: {locator}")
        element = self.find_element(locator)
        self.actions.context_click(element).perform()

    # --- Input Actions ---
    def enter_text(self, locator, text):
        logger.info(f"Entering text '{text}' into element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        text = self.find_element(locator).text
        logger.info(f"Text found: {text}")
        return text

    def get_attribute(self, locator, attribute):
        value = self.find_element(locator).get_attribute(attribute)
        logger.info(f"Attribute '{attribute}' value: {value}")
        return value

    # --- Select Actions ---
    def select_by_visible_text(self, locator, text):
        logger.info(f"Selecting '{text}' from dropdown: {locator}")
        select = Select(self.find_element(locator))
        select.select_by_visible_text(text)

    def select_by_value(self, locator, value):
        logger.info(f"Selecting value '{value}' from dropdown: {locator}")
        select = Select(self.find_element(locator))
        select.select_by_value(value)

    def select_by_index(self, locator, index):
        logger.info(f"Selecting index '{index}' from dropdown: {locator}")
        select = Select(self.find_element(locator))
        select.select_by_index(index)

    # --- ActionChains & Mouse Actions ---
    def hover(self, locator):
        logger.info(f"Hovering over element: {locator}")
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()

    def drag_and_drop(self, source_locator, target_locator):
        logger.info(f"Dragging from {source_locator} to {target_locator}")
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        self.actions.drag_and_drop(source, target).perform()

    # --- Keyboard Actions ---
    def press_key(self, locator, key):
        """Example: press_key(locator, Keys.ENTER)"""
        logger.info(f"Pressing key on element: {locator}")
        self.find_element(locator).send_keys(key)

    def select_all_and_delete(self, locator):
        logger.info(f"Selecting all and deleting text in: {locator}")
        element = self.find_element(locator)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    # --- JavaScript Actions ---
    def js_click(self, locator):
        logger.info(f"JavaScript clicking on element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, locator):
        logger.info(f"Scrolling to element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def js_execute(self, script, *args):
        logger.info(f"Executing script: {script}")
        return self.driver.execute_script(script, *args)

    # --- Verification Actions ---
    def is_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def is_enabled(self, locator):
        return self.find_element(locator).is_enabled()

    def is_selected(self, locator):
        return self.find_element(locator).is_selected()

    # --- Screenshot & Reporting ---
    def take_screenshot(self, name):
        if not os.path.exists("reports/screenshots"):
            os.makedirs("reports/screenshots")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = f"reports/screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved to {path}")
        return path

    def attach_screenshot_to_allure(self, name):
        """Attach screenshot to Allure report if allure is installed."""
        try:
            import allure
            path = self.take_screenshot(name)
            allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
        except ImportError:
            logger.warning("Allure not installed, skipping attachment.")

    # --- Window & Frame Actions ---
    def switch_to_frame(self, locator):
        logger.info(f"Switching to frame: {locator}")
        element = self.find_element(locator)
        self.driver.switch_to.frame(element)

    def switch_to_default_content(self):
        logger.info("Switching to default content")
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle):
        logger.info(f"Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)
