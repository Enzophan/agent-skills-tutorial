Feature: an error message with invalid credentials
  As a user
  I want to see the homepage with invalid credentials
  So that the application behaves correctly

  @homepage @smoke
  Scenario: User can access the homepage with invalid credentials
    Given the user is on the "DEV Community" page
    When the user clicks on the "Site Logo" image.
    Then the user should be redirected to the "Home" page

  @homepage
  Scenario: User can access the DEV Challenges page
    Given the user is on the "DEV Community" page
    When the user clicks on the "DEV Challenges" link.
    Then the user should be redirected to the "DEV Challenges" page

   
  Scenario: User can access the DEV Education Tracks page
    Given the user is on the "DEV Community" page
    When the user clicks on the "DEV Education Tracks" link.
    Then the user should be redirected to the "DEV Education Tracks" page
