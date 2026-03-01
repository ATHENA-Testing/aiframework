from behave import given, when, then

@given('I am on the Amazon homepage')
def step_impl(context):
    context.browser.get("https://www.amazon.com")

from behave import when

@when('I navigate to Mobiles - Smartphones')
def step_impl(context):
    context.page.navigate_to_mobiles_smartphones()

from behave import then

@then('I should see the smartphone listings page')
def step_impl(context):
    context.page.should_see_smartphone_listings_page()

from behave import given

@given('I am on the Smartphones listing page')
def step_impl(context):
    context.page.navigate_to_mobiles_smartphones()
    context.page.should_see_smartphone_listings_page()

from behave import when

@when("I apply a price filter of Up to {price:d}")
def step_impl(context, price):
    # Assuming context has a page object with a method to apply the price filter,
    # since no specific method is listed in the provided Page Object Methods,
    # implement a placeholder or raise an error to indicate not implemented.
    if hasattr(context, "page") and hasattr(context.page, "apply_price_filter_up_to"):
        context.page.apply_price_filter_up_to(price)
    else:
        raise NotImplementedError("Method to apply price filter is not implemented in the page object.")

from behave import then

@then('only smartphones priced at or below 30000 are shown')
def step_impl(context):
    context.navigate_to_mobiles_smartphones()
    context.should_see_smartphone_listings_page()
    results = context.get_results_text()
    # Assuming results is a list of dict with 'price' key or a parsable string
    # Example: [{'name': 'Phone X', 'price': 29999}, ...]
    for item in results:
        price = item.get('price', 0)
        assert price <= 30000, f"Found smartphone priced above 30000: {price}"

from behave import given

@given('the price filter is applied')
def step_impl(context):
    # Implement applying the price filter using available page object methods or direct context manipulation
    # Assuming there is a method to apply price filter - if not, implement accordingly
    # Example placeholder implementation:
    context.page.apply_price_filter()  # Replace with actual method if exists

@when('the results reload')
def step_impl(context):
    # Implement how the results reload - this depends on application specifics,
    # for example, could be refreshing the page or triggering reload via JS etc.
    # Placeholder example:
    context.page.reload_results()

@then('the number of products updates accordingly')
def step_impl(context):
    # Implement validation that the number of products updates accordingly.
    # Example: compare the product count before and after some action.
    # Assuming 'context' stores previous and current product counts.
    previous_count = getattr(context, 'previous_product_count', None)
    current_count = context.page.get_results_count()  # hypothetical method
    
    assert previous_count is not None, "Previous product count not set in context"
    assert current_count != previous_count, "Product count did not update accordingly"

@given('filtered products are displayed')
def step_filtered_products_are_displayed(context):
    # Assuming filtered products are displayed after navigating to mobiles smartphones page
    context.navigate_to_mobiles_smartphones()
    context.should_see_smartphone_listings_page()

from behave import then

@then('each product has a listed price less than or equal to 30000 before coupons')
def step_impl(context):
    for product in context.products:
        assert product.listed_price <= 30000, f"Product price {product.listed_price} exceeds 30000"

from behave import then

@then('each product has a listed price less than or equal to 30000 (before coupons)')
def step_impl(context):
    # Assuming context.page has a method to verify product prices
    assert context.page.all_products_price_at_most(30000), \
        "Not all products have a listed price <= 30000 (before coupons)"
