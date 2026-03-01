Feature: Purchase a smartphone under 30000 on Amazon by applying filters

  As a price-conscious shopper,
  I want to find and purchase a smartphone under 30000 on Amazon
  by filtering products based on price, ratings, and reviews,
  so that I can compare top-rated options within my budget and make a confident purchase.

  Background:
    Given I am on the Amazon homepage

  Scenario: Navigate to Mobiles - Smartphones category
    When I navigate to Mobiles - Smartphones
    Then I should see the smartphone listings page

  Scenario: Apply price filter for smartphones up to 30000
    Given I am on the Smartphones listing page
    When I apply a price filter of Up to 30000
    Then only smartphones priced at or below 30000 are shown

  Scenario: Verify product count updates after applying price filter
    Given the price filter is applied
    When the results reload
    Then the number of products updates accordingly

  Scenario: Validate each filtered smartphone price before coupons
    Given filtered products are displayed
    Then each product has a listed price less than or equal to 30000 (before coupons)