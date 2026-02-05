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
