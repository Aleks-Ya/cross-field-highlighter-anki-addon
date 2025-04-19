#noinspection CucumberUndefinedStep
Feature: Using earliest Anki version 24.6.3

  @smoke @browser @editor
  Scenario: Use in Anki 24.6.3

    Given I opened Anki 24.6.3 Qt5
    And I deleted addon
    And I installed previous version by ID 1312127886
    And I restarted Anki
    And I installed latest version from file
    And I restarted Anki
    Then Anki started without errors