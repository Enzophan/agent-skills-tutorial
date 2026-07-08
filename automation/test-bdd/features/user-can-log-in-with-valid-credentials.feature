Feature: log in with valid credentials
  As a user
  I want to log in with valid credentials
  So that the application behaves correctly

  @user-login @smoke
  Scenario: User can log in with valid credentials
    Given the user is on the relevant page
    When the user performs the action for "User can log in with valid credentials"
    Then the expected outcome for "User can log in with valid credentials" is displayed
