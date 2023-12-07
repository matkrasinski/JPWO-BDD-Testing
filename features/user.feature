Feature: User authorization
  BDD tests for user login and registration

  Scenario: User registers successfully
    Given I run Chrome Browser
    And I go to the registration page from home page
    When I fill registration form with valid random data
    And I press "Register" button
    Then I am on the login page

  Scenario: User registers using existing email
    Given I run Chrome Browser
    And I go to the registration page from home page
    When I fill registration form with valid random data
    And I press "Register" button
    Then I am on the login page
    When I go to registration page from login page
    Then I fill registration form with latest email
    And I press "Register" button
    Then I see error message about existing email

  Scenario: User registers with invalid date of birth
    Given I run Chrome Browser
    And I go to the registration page from home page
    When I fill registration form with random data containing invalid date of birth
    And I press "Register" button
    Then I see error message about invalid date of birth