from behave import given, when, then
from selenium.webdriver.common.by import By

from pages.example_page import ExamplePage
import yaml

from pages.user_story_page import login_as_pcd_user, search_to_checkout


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


class SearchPage:
    pass


@given("I am on the search page")
def step_given_i_am_on_the_search_page(context):
    context.search_page = SearchPage(context)

@when("I search for '{term}'")
def step_when_i_search_for_term(context, term):
    context.search_page.search(term)

@then("I should see search results")
def step_then_i_should_see_search_results(context):
    assert context.search_page.is_search_results_visible()

@given("the user attempts to proceed to Step 2")
def step_given_the_user_attempts_to_proceed_to_step_2(context):
    pass  # No action required as per your provided methods

@then("{statements} have been entered")
def step_then_statements_have_been_entered(context, statements):
    pass  # Implement this step based on the specific statements and available context data


class LoginPage:
    pass


class DashboardPage:
    pass


@when("I search for '{term}' and I am logged into the virtual deal desk as a PCD user with username {username}")
def step_when_i_search_for_term_and_i_am_logged_in(context, term, username):
    context.login_page = LoginPage(context)
    context.dashboard_page = DashboardPage(context)

    # Log in as PCD user with provided username
    login_as_pcd_user(username)

    # Proceed to search and checkout process (if applicable)
    search_to_checkout(term)

@then("the user should be on Step 2")
def step_then_the_user_should_be_on_step_2(context):
    assert context.dashboard_page.is_on_step_2()
