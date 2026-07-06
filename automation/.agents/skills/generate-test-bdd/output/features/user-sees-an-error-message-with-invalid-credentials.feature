Feature: an error message with invalid credentials
  As a user
  I want to an error message with invalid credentials
  So that the application behaves correctly

  Scenario: User sees an error message with invalid credentials
    Given the user is on the relevant page
    When the user performs the action for "User sees an error message with invalid credentials"
    Then the expected outcome for "User sees an error message with invalid credentials" is displayed
