Feature: reset their password via email
  As a user
  I want to reset their password via email
  So that the application behaves correctly

  @user-login @uat
  Scenario: User can reset their password via email
    Given the user is on the relevant page
    When the user performs the action for "User can reset their password via email"
    Then the expected outcome for "User can reset their password via email" is displayed
