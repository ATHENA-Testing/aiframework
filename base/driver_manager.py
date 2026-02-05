import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverManager:
    @staticmethod
    def get_driver():
        with open("config/framework.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        browser = config.get('browser', 'chrome').lower()
        headless = config.get('headless', False)
        
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
            
        driver.maximize_window()
        driver.implicitly_wait(config.get('timeout', 30))
        return driver
