Feature: Example Search Feature
  As a user
  I want to search on Google
  So that I can find information

  Scenario: Search for a term
    Given I am on the search page
    When I search for "Python Selenium BDD"
    Then I should see search results
