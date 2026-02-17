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

@given('a user with username "{username}"')
def step_impl(context, username):
    context.login_as_pcd_user(username)

from behave import given

@given('a user with username "{username}"')
def step_impl(context, username):
    context.login_as_pcd_user(username)

@when('the user enters PIN "{pin}"')
def step_impl(context, pin):
    # Implement the action to enter the PIN; assuming a page object method context.page.enter_pin exists
    context.page.enter_pin(pin)

@then("the system verifies the PIN is valid")
def step_impl(context):
    # Implementation depends on context, assuming a method context.system.verify_pin()
    assert context.system.verify_pin() is True, "PIN verification failed"

from behave import given

@given('a user with username "{username}"')
def step_impl(context, username):
    context.login_as_pcd_user(username)

@when('the user selects the withdrawal amount "{amount}"')
def step_impl(context, amount):
    # Implement selection of withdrawal amount here
    context.page.select_withdrawal_amount(amount)

@then('the system verifies if the user has sufficient balance')
def step_verify_sufficient_balance(context):
    # Implement verification logic here, for example:
    # user_balance = context.user.get_balance()
    # required_amount = context.transaction.amount
    # assert user_balance >= required_amount, "Insufficient balance"
    pass

from behave import given

@given('a user with username "{username}"')
def step_impl(context, username):
    context.login_as_pcd_user(username)

@then('the system confirms sufficient balance')
def step_confirm_sufficient_balance(context):
    # TODO: Implement balance confirmation logic here
    pass

from behave import when

@when('the system dispenses the cash amount "{amount}"')
def step_impl(context, amount):
    # Implement logic to simulate cash dispensing
    context.cash_dispensed = int(amount)
    # Here you can add any interaction with your system to simulate dispensing cash
    pass

@then("the user's account balance is updated accordingly")
def step_account_balance_updated(context):
    # Implementation depends on how account balance is stored and accessed in context or page objects.
    # Placeholder example:
    expected_balance = context.expected_balance
    actual_balance = context.account_page.get_account_balance()
    assert actual_balance == expected_balance, f"Expected balance {expected_balance}, but got {actual_balance}"

@given('a user with username "{username}"')
def step_impl(context, username):
    context.login_as_pcd_user(username)

@then('the system has dispensed the cash amount "{amount}"')
def step_impl(context, amount):
    # Implementation placeholder: verify that the system dispensed the specified cash amount
    dispensed_amount = context.atm.get_dispensed_cash()  # Assuming context.atm exists and has this method
    assert dispensed_amount == amount, f"Expected dispensed amount to be {amount} but got {dispensed_amount}"

@when('the user requests a receipt')
def step_impl(context):
    # Implement the action where the user requests a receipt
    context.page.request_receipt()

@then('the system provides a receipt for the withdrawal')
def step_impl(context):
    # Implement receipt verification logic here
    receipt = context.system.get_withdrawal_receipt()
    assert receipt is not None, "No receipt was provided for the withdrawal"

@given('a user with username "{username}"')
def step_impl(context, username):
    context.login_as_pcd_user(username)

@then('the system has dispensed the cash amount "{amount}"')
def step_impl(context, amount):
    # Implement the check or simulation that the system has dispensed the cash amount
    dispensed_amount = context.system.get_dispensed_cash()  # Example method, replace with actual
    assert str(dispensed_amount) == amount, f"Expected dispensed amount {amount}, but got {dispensed_amount}"

@then('the system does not provide a receipt')
def step_system_does_not_provide_receipt(context):
    # Implement verification that no receipt is provided by the system.
    # This could be checking the absence of a receipt element or message.
    receipt_present = hasattr(context, 'receipt') and context.receipt.is_displayed()
    assert not receipt_present, "Expected no receipt to be provided, but receipt was found."
