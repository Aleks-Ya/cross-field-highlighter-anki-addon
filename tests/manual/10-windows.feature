#noinspection CucumberUndefinedStep
Feature: Work on Windows OS

  @smoke @browser
  Scenario: Run addon on Windows 10
    Given I deleted addon
    And I installed previous version by ID 1312127886
    And I restarted Anki
    And I installed latest version from distribution
    And I restarted Anki
    Then Anki started without errors
