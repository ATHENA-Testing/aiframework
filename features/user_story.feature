Feature: ATM Cash Withdrawal
  As a bank customer,
  I want to withdraw cash from an ATM,
  So that I can have physical currency.

  Background:
    Given I have inserted my card

  Scenario: Successful cash withdrawal with sufficient balance and receipt requested
    Given I enter a valid PIN "1234"
    When I select to withdraw an amount of 500
    And the system verifies sufficient balance
    Then the system dispenses cash of 500
    And the system updates my account balance accordingly
    And I request a receipt
    Then I receive a receipt for the transaction

  Scenario: Cash withdrawal denied due to insufficient balance
    Given I enter a valid PIN "1234"
    When I select to withdraw an amount of 500
    And the system verifies insufficient balance
    Then the system denies the withdrawal
    And I do not receive cash

  Scenario: Card insertion and invalid PIN entry lockout after 3 failed attempts
    Given I enter an invalid PIN "0000"
    And I enter an invalid PIN "1111"
    And I enter an invalid PIN "2222"
    Then my account is locked for 15 minutes
    And the system denies further withdrawal attempts

  Scenario: User requests cash withdrawal without requesting receipt
    Given I enter a valid PIN "1234"
    When I select to withdraw an amount of 500
    And the system verifies sufficient balance
    Then the system dispenses cash of 500
    And the system updates my account balance accordingly
    And I do not request a receipt
    Then I do not receive a receipt