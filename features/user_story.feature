Feature: Payer Strategy Workflow

  As a Pricing, Contracting, and Distribution (PCD) user,
  In order to define price protection policy and Brand Segment strategies in the Payer space,
  I want a dynamic interface to accurately capture varying max concession rate requirements.

Background:
  Given I am logged into the virtual deal desk as a PCD user with username [Strategy1]@example.com
  And the product is [Xolair]
  And the page is on the Payer Strategy creation form

Scenario: Target Account List Validation

  Scenario Outline: Testing the Target Account List validation
    Given the "limit this strategy to a limited target account list" option is <option>
    And the "Target Account List" contains <account_list>
    When the user attempts to proceed to Step 2.
    Then the system <result>

    Examples:
      | option       | account_list                             | result                            |
      | enabled       | ["Account1", "Account2"]                     | allows the user to proceed          |
      | enabled       | []                                           | displays error message and prevents proceeding  |
      | disabled       | ["Account1", "Account2"]                     | allows the user to proceed          |

Scenario: Formulary Positioning Statement Validation

  Scenario Outline: Testing the Formulary Positioning Statements validation
    Given <statements> have been entered.
    When the user attempts to proceed to Step 2.
    Then the system <result>

    Examples:
      | statements            | result                            |
      | ["Positioning Statement 1", "Positioning Statement 2"]       | allows the user to proceed          |
      | []                           | displays error message and prevents proceeding  |

Scenario: Login with Invalid Email Address or Incorrect Password
  Given I have entered an invalid email address "<invalid_email>" for login
  When I attempt to log in
  Then the system displays the error message "Invalid email or password"

Scenario: Login with Valid Credentials
  Given I have entered a valid email address "[Strategy1]@example.com" and password "<password>" for login
  When I attempt to log in
  Then I am able to successfully log in