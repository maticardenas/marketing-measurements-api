
Feature: Marketing Measurements
  Retrieve marketing measurements through API.

  Scenario: Retrieve marketing measurements for specific channel
    Given a set of existing conversions for marketing campaigns
    When requesting marketing measurements through API for a specific channel
    Then I should receive a list of measurements for that channel
