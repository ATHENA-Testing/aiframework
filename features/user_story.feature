Feature: Payer Strategy Workflow

  Scenario: Target Account List Validation
    Given a logged in user with username "[Strategy1]"
    And a product to define a strategy for, "[Xolair]"
    And the "limit this strategy to a limited target account list" option is enabled

    Scenario Outline: Validating Target Account List
      Given the "Target Account List" contains <accountCount> accounts
      When the user attempts to proceed to Step 2
      Then
        | Error Message              | Expected Result                            |
        | ""                          | The system allows user to proceed         |
        | "A Target Account List is required when limiting this strategy to specific accounts." | The system displays error and prevents user from proceeding if the list is empty or null |

    Examples:
      | accountCount   |
      | 1              |
      | 3              |
      | 0              |
      | null           |

  Scenario: Formulary Positioning Statement Validation
    Given a logged in user with username "[Strategy1]"
    And a product to define a strategy for, "[Xolair]"

    Scenario Outline: Validating Formulary Positioning Statements
      Given <statementCount> "Formulary Positioning Statements" have been entered

      When the user attempts to proceed to Step 2
      Then
        | Error Message              | Expected Result                            |
        | ""                          | The system allows user to proceed         |
        | "At least one Formulary Positioning Statement is required for this strategy." | The system displays error and prevents user from proceeding if no statements have been entered  |

    Examples:
      | statementCount |
      | 1              |
      | 0              |