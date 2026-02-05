# E-commerce Domain Knowledge

## Login Rules
- Usernames must be valid email addresses.
- Passwords must be at least 8 characters and include a special character.
- After 3 failed attempts, the account is locked for 15 minutes.

## Element Selectors (Preferred)
- Use `data-testid` attributes whenever available.
- For the login button, use `[data-testid='login-submit']`.
- For the search bar, use `id='search-input-main'`.

## Common Workflows
1. **Search to Checkout**: User searches for item -> adds to cart -> goes to checkout -> enters payment -> confirms order.
2. **Account Registration**: User clicks signup -> enters details -> verifies email -> login.
