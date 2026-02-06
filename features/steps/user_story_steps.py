from behave import given, when, then

from features.steps.example_steps import SearchPage, LoginPage, DashboardPage


# from pages.login_page import LoginPage
# 
# from pages.virtual_deal_desk import VirtualDealDesk
# from behave import given, when, then
# from pages.search_page import SearchPage
# from pages.login_page import LoginPage
# from pages.dashboard_page import DashboardPage
# from pages.virtual_deal_desk_pcd import VirtualDealDeskPcd
# from pages.search_page import SearchPage
# 
# from my_page_object import MyPage
# 
# from behave import given, when, then
# from pages.search_page import SearchPage
# from pages.login_page import LoginPage
# from pages.dashboard_page import DashboardPage
# from virtual_deal_desk import VirtualDealDesk
# 
# from pages.virtual_deal_desk_pcd_user_page import VirtualDealDeskPCDUserPage
# 
# from pages.virtual_deal_desk_login_page import VirtualDealDeskLoginPage
# from pages.virtual_deal_desk_dashboard_page import VirtualDealDeskDashboardPage


class VirtualDealDesk:
    pass


@given("I am logged into the virtual deal desk as a PCD user with username {username}")
def step_logged_in(context, username):
    if context.browser is None:
        raise Exception("# Browser not set")

    vdd = VirtualDealDesk(context.browser)
    login_page = vdd.go_to_login()

    # Assuming the login page has a method to fill in username and password, e.g., fill_credentials()
    if callable(getattr(login_page, "fill_username")):
        login_page.fill_username(f"{username}")

    # Assuming the login page has a method to submit the form, e.g., submit_form()
    if callable(getattr(login_page, "submit_form")):
        login_page.submit_form()

    # Wait for the search page to load and assert successful login
    vdd.assert_logged_in(username)


@given(u'the "limit this strategy to a limited target account list" option is {option}')
def step_given_limit_strategy(context, option):
    search_page = context.search_page
    if option:
        search_page.click_limit_strategy_target_account_list()
        search_page.enter_target_accounts(option)
    else:
        search_page.click_uncheck_limit_strategy_target_account_list()
    context.search_page = search_page


@when(u'I search for "{term}"')
def step_when_i_search(context, term):
    context.search_page.enter_search_query(term)
    context.search_page.click_search_button()


@then(u'I should see search results')
def step_then_i_should_see_results(context):
    assert context.search_page.is_search_results_visible(), "Search results are not visible"


class MyPage:
    pass


@given("the user attempts to proceed to Step 2")
def step_attempts_to_proceed(context):
    # This step doesn't directly use the Page Object methods provided, so we assume that there is a way
    # to navigate to the next step (e.g., clicking a button or link) within your application.
    context.my_page = MyPage()  # Assuming you have an instance of the page object for the current step
    context.my_page.navigate_to_next_step()  # Navigate to the next step (assuming this method exists in your Page Object)


@then("the user should be on Step 2")
def then_user_is_on_step_two(context):
    # If you have a way of verifying that the user is on Step 2 within your application,
    # implement it here. For now, we'll assume there's a method for checking this in your Page Object.
    context.my_page.assert_on_step_two()  # Assuming you have an assert_on_step_two() method in your Page Object


@given("{statements} have been entered")
def step_given_statements_have_been_entered(context):
    # Assuming 'statements' refers to the data or actions that need to be performed on the search page
    # This is a placeholder, you should replace it with specific actions using Page Object methods.
    if hasattr(SearchPage, context.current_step.name):
        return f"# Step '{context.current_step.name}' already exists."

    # Example implementation: entering search terms
    if 'statements' in context.examples_table:
        for statement in context.examples_table[context.current_scenario].rows:
            search_page = SearchPage(context)
            search_page.enter_search_terms(statement['statements'])


@when("I search for '{term}'")
def step_search(context, term):
    context.page.search(term)


@then("the system should display search results")
def step_display_results(context):
    results = context.page.get_search_results()
    if not results:
        raise AssertionError("# No search results found.")


@then("the system <result>")
def then_system_result(context, result):
    if callable(result):
        assert result(context)
    else:
        assert context.page.get_system_status() == result, f"Expected system status to be '{result}', but got '{context.page.get_system_status()}'."


@given("I have entered an invalid email address '<invalid_email>' for login")
def step_enter_invalid_email(context):
    # Assuming we have a LoginPage object (not provided in your requirements)
    login_page = context.login_page  # For simplicity, assuming it's already set up
    login_page.enter_email('<invalid_email>')
    login_page.submit()


@then("I should be on the search page")
def step_on_search_page(context):
    assert isinstance(context.current_page, SearchPage)


# For this example, I'm assuming the step "I am on the search page" is already defined and works as expected


@given("I am on the login page")
def step_given_i_am_on_the_login_page(context):
    context.login_page = LoginPage(context)
    context.login_page.open()


@when("I attempt to log in with valid credentials")
def step_when_i_attempt_to_log_in(context):
    context.login_page.fill_username_and_password()
    context.login_page.submit_form()


@then("I should be redirected to the dashboard page")
def step_then_i_should_be_redirected_to_the_dashboard_page(context):
    assert context.browser.current_url == LoginPage.DASHBOARD_URL, "Expected to be on the dashboard page."


@given("I am on the login page")
def step_impl(context):
    context.login_page = LoginPage(context)
    context.login_page.open()


@when("I enter an invalid email or password")
def step_impl(context):
    context.login_page.enter_invalid_email_or_password()


@then("the system displays the error message 'Invalid email or password'")
def step_impl(context):
    assert context.login_page.is_error_message_displayed('Invalid email or password')

@given("the 'Target Account List' contains {accountCount} accounts")
def step_target_account_list(context, accountCount):
    # This step doesn't have a corresponding Page Object method, so you'll need to implement it in your tests.
    pass

@when("I am on the search page")
def step_on_search_page(context):
    context.search_page = SearchPage(context)

@when("I search for '{term}'")
def step_search_for(context, term):
    context.search_page.search(term)

@then("I should see search results")
def step_see_search_results(context):
    assert context.search_page.is_search_results_displayed()

@when("the user attempts to proceed to Step 2")
def step_proceed_to_step_2(context):
    # This step doesn't have a corresponding Page Object method, so you'll need to implement it in your tests.
    pass

@when("{statements} have been entered")
def step_enter_statements(context, statements):
    # This step doesn't have a corresponding Page Object method, so you'll need to implement it in your tests.
    pass

@when("I search for '{term}' and I am logged into the virtual deal desk as a PCD user with username {username}")
def step_search_and_logged_in(context, term, username):
    context.login_page = LoginPage(context)
    context.dashboard_page = DashboardPage(context)
    context.login_page.navigate()
    context.login_page.login(username)
    context.search_page.search(term)

@then("the user should be on Step 2")
def step_on_step_2(context):
    assert context.dashboard_page.is_step_2_displayed()

@when("I am logged into the virtual deal desk as a PCD user with username {username}")
def step_logged_in(context, username):
    context.login_page = LoginPage(context)
    context.login_page.navigate()
    context.login_page.login(username)

@then("the system should display search results")
def step_display_search_results(context):
    assert context.search_page.is_search_results_displayed()

@when("the system <result>")
def step_system_result(context, result):
    # This step doesn't have a corresponding Page Object method, so you'll need to implement it in your tests.
    pass

@when("I have entered an invalid email address '<invalid_email>' for login")
def step_enter_invalid_email(context, invalid_email):
    context.login_page.fill_email_input(invalid_email)

@then("I should be on the search page")
def step_on_search_page_again(context):
    assert context.search_page.is_current()

@when("I am on the login page")
def step_on_login_page(context):
    context.login_page = LoginPage(context)

@when("I attempt to log in with valid credentials")
def step_attempt_valid_login(context):
    context.login_page.fill_and_submit()

@then("I should be redirected to the dashboard page")
def step_redirected_to_dashboard(context):
    assert context.dashboard_page.is_current()

@when("I enter an invalid email or password")
def step_enter_invalid_credentials(context):
    context.login_page.fill_and_submit_invalid()

@then("the system displays the error message 'Invalid email or password'")
def step_display_error_message(context):
    assert context.login_page.is_error_message_displayed('Invalid email or password')

#Here are the Behave step definitions in Python based on your requirements:



@given("I am on the search page")
def step_given_i_am_on_the_search_page(context):
    context.search_page = SearchPage()
    context.search_page.open()

@when("I search for '{term}'")
def step_when_i_search_for(context, term):
    context.search_page.search(term)

@then("I should see search results")
def step_then_i_should_see_search_results(context):
    assert context.search_page.is_search_results_visible(), "Search results not visible."

@when("the user attempts to proceed to Step 2")
def step_when_the_user_attempts_to_proceed_to_step_2(context):
    pass  # No specific action needed, as it's part of the user flow.

@then("{statements} have been entered")
def step_then_statements_have_been_entered(context, statements):
    assert context.user_flow.statements_are_entered(statements), "Incorrect statements entered."

@when("I search for '{term}' and I am logged into the virtual deal desk as a PCD user with username {username}")
def step_when_i_search_for_and_i_am_logged_in(context, term, username):
    context.virtual_deal_desk = VirtualDealDesk()
    context.virtual_deal_desk.login_as_pcd_user(username)
    context.search_page.search(term)

@then("the user should be on Step 2")
def step_then_the_user_should_be_on_step_2(context):
    assert context.current_step == 2, "User not on Step 2."

@when("I am logged into the virtual deal desk as a PCD user with username {username}")
def step_when_i_am_logged_in(context, username):
    context.virtual_deal_desk = VirtualDealDesk()
    context.virtual_deal_desk.login_as_pcd_user(username)

@then("the system should display search results")
def step_then_the_system_should_display_search_results(context):
    assert context.virtual_deal_desk.is_search_results_visible(), "Search results not visible."

@when("the system <result>")
def step_when_the_system_result(context, result):
    # Custom action based on the result string. Implement this in your test flow.
    pass

@when("I have entered an invalid email address '<invalid_email>' for login")
def step_when_i_have_entered_an_invalid_email_address(context, invalid_email):
    context.login_page = LoginPage()
    context.login_page.enter_email(invalid_email)

@then("I should be on the search page")
def step_then_i_should_be_on_the_search_page(context):
    assert context.current_url == context.search_page.url, "Not on the search page."

@when("I am on the login page")
def step_when_i_am_on_the_login_page(context):
    context.login_page = LoginPage()

@when("I attempt to log in with valid credentials")
def step_when_i_attempt_to_log_in_with_valid_credentials(context):
    valid_email, valid_password = context.credentials.get_valid_pcd_credentials()
    context.login_page.enter_email(valid_email)
    context.login_page.enter_password(valid_password)
    context.login_page.submit_form()

@then("I should be redirected to the dashboard page")
def step_then_i_should_be_redirected_to_the_dashboard_page(context):
    assert context.current_url == context.dashboard_page.url, "Not redirected to the dashboard page."

@when("I enter an invalid email or password")
def step_when_i_enter_an_invalid_email_or_password(context):
    invalid_credentials = context.credentials.get_invalid_pcd_credentials()
    context.login_page.enter_email(invalid_credentials["email"])
    context.login_page.enter_password(invalid_credentials["password"])
    context.login_page.submit_form()

@then("the system displays the error message 'Invalid email or password'")
def step_then_the_system_displays_the_error_message(context):
    assert context.login_page.is_invalid_email_or_password_error_visible(), "Error message not displayed."

#Here are the Behave step definitions for your requirements:


class VirtualDealDeskPCDUserPage:
    pass


@given("a logged in user with username {username}")
def step_given_logged_in_user(context, username):
    context.search_page = SearchPage(context)
    context.virtual_deal_desk_pcd_user_page = VirtualDealDeskPCDUserPage(context)

    # Log in as a PCD user with the provided username and navigate to the virtual deal desk
    context.login_page = LoginPage(context)
    context.login_page.navigate()
    context.login_page.enter_username(username)
    context.login_page.enter_password('secret')  # Replace 'secret' with the actual password for PCD users
    context.login_page.click_login()
    context.virtual_deal_desk_pcd_user_page.wait_for_page_to_load()

@when("the user attempts to proceed to Step 2")
def step_when_proceed_to_step_2(context):
    context.virtual_deal_desk_pcd_user_page.click_step_2_link()

@then("I should be on Step 2")
def step_then_on_step_2(context):
    assert context.virtual_deal_desk_pcd_user_page.is_on_step_2(), "User is not on Step 2"

@when("{statements} have been entered")
def step_when_statements_entered(context, statements):
    # This step requires specific implementation based on the provided statements.
    # As it's not provided, I'm assuming that this is an empty step for now.
    pass

#Here are the Behave step definitions in Python based on your requirements:




@given("I am on the search page")
def step_given_i_am_on_the_search_page(context):
    context.search_page = SearchPage()
    context.search_page.open()

@when("{user} searches for '{term}'")
def step_when_searches_for_something(context, user, term):
    context.search_page.search(term)

@then("I should see search results")
def step_then_i_should_see_search_results(context):
    context.search_page.assert_search_results_displayed()

@when("the user attempts to proceed to Step 2")
def step_when_user_attempts_to_proceed_to_step_2(context):
    pass  # No Page Object method available for this step

@given("<statementCount> 'Formulary Positioning Statements' have been entered")
def step_given_statements_have_been_entered(context, statementCount):
    pass  # No Page Object method available for this step


class VirtualDealDeskLoginPage:
    pass


@when("{user} searches for '{term}' and I am logged into the virtual deal desk as a PCD user with username {username}")
def step_when_searches_for_something_and_logged_in(context, user, term, username):
    context.virtual_deal_desk_login_page = VirtualDealDeskLoginPage()
    context.virtual_deal_desk_login_page.login_as_pcd_user(username)
    context.search_page = SearchPage()
    context.search_page.open()
    context.search_page.search(term)

@then("the user should be on Step 2")
def step_then_user_should_be_on_step_2(context):
    pass  # No Page Object method available for this step

@then("the system should display search results")
def step_then_system_should_display_search_results(context):
    context.search_page.assert_search_results_displayed()

@when("I enter an invalid email address '<invalid_email>' for login")
def step_when_enters_an_invalid_email_address(context, invalid_email):
    context.virtual_deal_desk_login_page = VirtualDealDeskLoginPage()
    context.virtual_deal_desk_login_page.enter_invalid_email(invalid_email)

@then("I should be on the search page")
def step_then_i_should_be_on_the_search_page(context):
    context.search_page = SearchPage()
    assert context.search_page.is_currently_displayed(), "Currently not on the search page"

@when("I am on the login page")
def step_when_i_am_on_the_login_page(context):
    context.virtual_deal_desk_login_page = VirtualDealDeskLoginPage()
    assert context.virtual_deal_desk_login_page.is_currently_displayed(), "Not on the login page"

@when("I attempt to log in with valid credentials")
def step_when_i_attempt_to_log_in_with_valid_credentials(context):
    context.virtual_deal_desk_login_page.login_with_valid_credentials()


class VirtualDealDeskDashboardPage:
    pass


@then("I should be redirected to the dashboard page")
def step_then_i_should_be_redirected_to_the_dashboard_page(context):
    context.virtual_deal_desk_dashboard_page = VirtualDealDeskDashboardPage()
    assert context.virtual_deal_desk_dashboard_page.is_currently_displayed(), "Not redirected to the dashboard page"

@when("I enter an invalid email or password")
def step_when_i_enter_an_invalid_email_or_password(context):
    context.virtual_deal_desk_login_page = VirtualDealDeskLoginPage()
    context.virtual_deal_desk_login_page.enter_invalid_credentials()

@then("the system displays the error message 'Invalid email or password'")
def step_then_system_displays_the_error_message(context):
    assert context.virtual_deal_desk_login_page.is_error_message_displayed(), "Error message not displayed"

#Here are the Behave step definitions in Python based on your requirements:




@given("I am on the search page")
def step_given_i_am_on_the_search_page(context):
    context.search_page = SearchPage()
    context.search_page.navigate_to()

@when("I search for '{term}'")
def step_when_i_search_for_term(context, term):
    context.search_page.search(term)

@then("I should see search results")
def step_then_i_should_see_search_results(context):
    context.search_page.assert_search_results_displayed()

@when("the user attempts to proceed to Step 2")
def step_when_the_user_attempts_to_proceed_to_step_2(context):
    # This step doesn't directly interact with the page objects, so it can't be defined here.
    pass

@then("{statements} have been entered")
def step_then_statements_have_been_entered(context, statements):
    # This step doesn't directly interact with the page objects, so it can't be defined here.
    pass


class VirtualDealDeskPcd:
    pass


@when("I search for '{term}' and I am logged into the virtual deal desk as a PCD user with username '{username}''")
def step_when_i_search_for_term_and_i_am_logged_into_the_virtual_deal_desk(context, term, username):
    context.login_page = LoginPage()
    context.dashboard_page = DashboardPage()
    context.virtual_deal_desk_pcd = VirtualDealDeskPcd()

    # Login to the virtual deal desk as a PCD user
    context.login_page.navigate_to()
    context.login_page.enter_username(username)
    context.login_page.enter_password('correct_password')  # Replace 'correct_password' with actual password for the PCD user.
    context.login_page.click_login_button()

    # Search for the term after successful login
    context.search_page = SearchPage()
    context.search_page.search(term)

@then("the user should be on Step 2")
def step_then_the_user_should_be_on_step_2(context):
    # This step doesn't directly interact with the page objects, so it can't be defined here.
    pass

@then("I am logged into the virtual deal desk as a PCD user with username '{username}'")
def step_then_i_am_logged_into_the_virtual_deal_desk(context, username):
    assert context.virtual_deal_desk_pcd.is_user_logged_in() and \
           context.virtual_deal_desk_pcd.get_username() == username

@then("the system should display search results")
def step_then_the_system_should_display_search_results(context):
    assert context.search_page.is_search_results_displayed()

@when("the system <result>")
def step_when_the_system_result(context, result):
    # This step doesn't directly interact with the page objects, so it can't be defined here.
    pass

@when("I have entered an invalid email address '<invalid_email>' for login")
def step_when_i_have_entered_an_invalid_email_address(context, invalid_email):
    context.login_page.enter_email(invalid_email)

@then("I should be on the search page")
def step_then_i_should_be_on_the_search_page(context):
    assert context.search_page.is_current()

@when("I am on the login page")
def step_when_i_am_on_the_login_page(context):
    context.login_page = LoginPage()
    context.login_page.navigate_to()

@when("I attempt to log in with valid credentials")
def step_when_i_attempt_to_log_in_with_valid_credentials(context):
    # Replace 'correct_email' and 'correct_password' with actual valid credentials for the PCD user.
    context.login_page.enter_email('correct_email')  # Replace 'correct_email' with actual email for the PCD user.
    context.login_page.enter_password('correct_password')  # Replace 'correct_password' with actual password for the PCD user.
    context.login_page.click_login_button()

@then("I should be redirected to the dashboard page")
def step_then_i_should_be_redirected_to_the_dashboard_page(context):
    assert context.dashboard_page.is_current()

@when("I enter an invalid email or password")
def step_when_i_enter_an_invalid_email_or_password(context):
    # Replace '<invalid_email>' and '<invalid_password>' with actual invalid credentials for the PCD user.
    context.login_page.enter_email('<invalid_email>')  # Replace '<invalid_email>' with actual invalid email for the PCD user.
    context.login_page.enter_password('<invalid_password>')  # Replace '<invalid_password>' with actual invalid password for the PCD user.
    context.login_page.click_login_button()

@then("the system displays the error message 'Invalid email or password'")
def step_then_the_system_displays_the_error_message(context):
    assert context.login_page.is_invalid_email_or_password_error_displayed()
