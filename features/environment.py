from base.driver_manager import DriverManager
from utils.logger import logger
import yaml

def before_all(context):
    logger.info("Starting Automation Suite...")
    with open("config/framework.yaml", 'r') as f:
        context.config = yaml.safe_load(f)

def before_scenario(context, scenario):
    logger.info(f"Starting Scenario: {scenario.name}")
    context.driver = DriverManager.get_driver()

def after_scenario(context, scenario):
    if scenario.status == "failed":
        if context.config.get('screenshot_on_failure', True):
            import os
            if not os.path.exists("reports/screenshots"):
                os.makedirs("reports/screenshots")
            screenshot_path = f"reports/screenshots/{scenario.name.replace(' ', '_')}.png"
            context.driver.save_screenshot(screenshot_path)
            logger.error(f"Scenario failed. Screenshot saved to {screenshot_path}")
    
    context.driver.quit()
    logger.info(f"Finished Scenario: {scenario.name}")

def after_all(context):
    logger.info("Automation Suite Execution Finished.")
