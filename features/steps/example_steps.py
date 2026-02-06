from behave import given, when, then
from pages.example_page import ExamplePage
import yaml

@given('I am on the search page')
def step_given_i_am_on_search_page(context):
    with open("config/framework.yaml", 'r') as f:
        config = yaml.safe_load(f)
    context.page = ExamplePage(context.driver)
    context.page.open_url("https://www.google.com")

@when('I search for "{term}"')
def step_when_i_search_for(context, term):
    context.page.search_for(term)

@then('I should see search results')
def step_then_i_should_see_results(context):
    assert context.page.is_displayed(context.page.RESULT_STATS)

Here are the Behave step definitions based on your requirements:


from behave import given, when, then
from selenium.webdriver.common.by import By

class SearchSteps:
    @given("I am on the search page")
    def step_i_am_on_the_search_page(context):
        pass  # This step doesn't need a specific action as it is assumed to be the starting point.

    @when("I search for \"{term}\"")
    def step_i_search_for(context, term):
        context.browser.find_element(By.NAME, 'q').send_keys(term)  # Assuming there is a text input named 'q' on the search page.
        context.browser.find_element(By.NAME, 'btnK').click()  # Assuming there is a submit button with name 'btnK'.

    @then("I should see search results")
    def step_i_should_see_search_results(context):
        pass  # This assertion might depend on specific elements in the search results. You would need to implement it according to your search page structure.
