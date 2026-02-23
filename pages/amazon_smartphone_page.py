from base.base_page import BasePage

class AmazonSmartphonePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_mobiles_smartphones(self):
        smartphones_category_locator = ("css selector", "[data-testid='category-mobiles-smartphones']")
        self.click(smartphones_category_locator)

    def should_see_smartphone_listings_page(self):
        locator = ("css selector", "[data-testid='smartphone-listings']")
        return self.is_displayed(locator)

    def apply_price_filter_up_to_30000(self):
        price_filter_locator = ("css selector", "[data-testid='price-filter-up-to-30000']")
        self.click(price_filter_locator)
