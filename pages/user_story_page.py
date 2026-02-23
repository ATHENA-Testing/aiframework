import hashlib
import string
import re
from selenium.webdriver.common.by import By
from base.base_page import BasePage

class UserStoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._base_url = "https://example.com" # Placeholder

    def login_as_pcd_user(self, strategy1):
        # Enter email address (strategy1@example.com)
        email_locator = (By.CSS_SELECTOR, '[data-testid="email"]')
        self.enter_text(email_locator, f"{strategy1}@example.com")

        # Enter password (min. 8 characters including a special character)
        password_locator = (By.CSS_SELECTOR, '[data-testid="password"]')
        self.enter_text(password_locator, "SecurePassword123!")
        
        # Click on the login button
        login_submit = (By.CSS_SELECTOR, '[data-testid="login-submit"]')
        self.click(login_submit)

        # Check for failed login attempts and account lock
        lock_message = (By.CSS_SELECTOR, '[data-testid="locked-account-message"]')
        if self.is_displayed(lock_message):
            raise Exception("Account is locked after 3 unsuccessful attempts.")

    def login(self, email, password):
        self.open_url(self._base_url)
        
        email_locator = (By.ID, 'email-input')
        self.enter_text(email_locator, email)

        password_locator = (By.ID, 'password-input')
        self.enter_text(password_locator, password)

        login_button_locator = (By.CSS_SELECTOR, '[data-testid="login-submit"]')
        self.click(login_button_locator)

    def search_to_checkout(self, product):
        search_input = (By.ID, 'search-input-main')
        self.enter_text(search_input, product)
        
        search_button = (By.XPATH, '//input[@id="search-input-main"]/following-sibling::button[1]')
        self.click(search_button)

        # Wait for the search results to load and click on the first item
        product_card = (By.XPATH, '//h3[@class="product-name"]/ancestor::div[contains(@class, "product-card")]')
        add_to_cart = (By.XPATH, '//h3[@class="product-name"]/ancestor::div[contains(@class, "product-card")]/descendant::button[@data-testid="add-to-cart"]')
        self.click(add_to_cart)

        # Go to the cart and click on the checkout button
        cart_link = (By.XPATH, '//a[@href="/cart"]')
        self.click(cart_link)
        
        checkout_button = (By.XPATH, '//button[contains(., "Checkout")]')
        self.click(checkout_button)

    def attempt_account_registration(self):
        self.click((By.ID, 'signup-button'))
        
        unique_email = f"user_{str(hashlib.md5(self.driver.current_url.encode()).hexdigest())}@example.com"
        self.enter_text((By.ID, 'email-input'), unique_email)
        self.enter_text((By.ID, 'password-input'), 'Password1$SpecialCharacter')
        
        self.click((By.ID, 'continue-button'))
        self.click((By.ID, 'confirm-button'))
