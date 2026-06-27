#noinspection CucumberUndefinedStep
Feature: Update addon

  Background:
  I built an addon distribution.

  @smoke @add
  Scenario: Dialog states are preserved during update

    Given I deleted addon
    And I installed previous version by ID 1312127886
    And I restarted Anki
    And I open "Add" window
    And I open "Highlight" dialog
    Then The state is
      | Format | "Bold" |

    When I choose
      | Format | "Yellow Background" |
    And I click "Cancel" button
    And I installed latest version from distribution
    And I restarted Anki
    Then Anki started without errors

    When I open "Add" window
    And I open "Highlight" dialog
    Then The state is
      | Format | "Yellow Background" |
