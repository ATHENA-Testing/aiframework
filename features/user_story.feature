Feature: ATM Cash Withdrawal
  As a bank customer,
  I want to withdraw cash from an ATM,
  So that I can have physical currency.

  Background:
    Given a user with username "[Strategy1]"

  Scenario: Insert card and enter valid PIN
    Given a user with username "[Strategy1]"
    When the user inserts their card into the ATM
    And the user enters PIN "1234"
    Then the system verifies the PIN is valid

  Scenario: Select withdrawal amount
    Given a user with username "[Strategy1]"
    And the user has successfully entered a valid PIN
    When the user selects the withdrawal amount "500"
    Then the system verifies if the user has sufficient balance

  Scenario: Sufficient balance verification and cash dispensing
    Given a user with username "[Strategy1]"
    And the user has selected the withdrawal amount "500"
    And the system confirms sufficient balance
    When the system dispenses the cash amount "500"
    Then the user's account balance is updated accordingly

  Scenario: Receipt issuance upon request
    Given a user with username "[Strategy1]"
    And the system has dispensed the cash amount "500"
    When the user requests a receipt
    Then the system provides a receipt for the withdrawal

  Scenario: Receipt not requested
    Given a user with username "[Strategy1]"
    And the system has dispensed the cash amount "500"
    When the user does not request a receipt
    Then the system does not provide a receipt