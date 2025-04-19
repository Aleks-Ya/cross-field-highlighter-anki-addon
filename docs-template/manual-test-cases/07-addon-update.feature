#noinspection CucumberUndefinedStep
Feature: Switch Profile
  "Highlight" and "Erase" windows states should be preserved during addon updates.

  Background:
  I built an addon distribution.

  @smoke @add
  Scenario: Update addon
    Given I deleted the addon
    And I installed the addon from distribution
    And I restarted Anki

    When I open "Add" window
    And I open "Highlight" dialog
    Then The state is
      | Format | "Bold" |

    When I choose
      | Format | "Yellow Background" |
    And I click "Cancel" button
    And I re-install the addon from distribution
    And I restart Anki
    And I open "Add" window
    And I open "Highlight" dialog
    Then The state is
      | Format | "Yellow Background" |
