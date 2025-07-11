#noinspection CucumberUndefinedStep
Feature: Highlight in Add Note window

  Background:
  Test "manual_test.py" was executed.
  Profile "CFH Manual Test 1" was opened.

  @smoke @add
  Scenario: Highlight and erase operations in Add Note window

    Given I opened the Add window
    And I chose "Basic" Note Type
    And I entered
      | Front | cat  |
      | Back  | cats |

    When I click "Highlight" button
    And I click "Select All" button
    And I click "Start" button
    Then The word "cats" is highlighted

    When I click "Erase" button
    And I click "Select All" button
    And I click "Start" button
    Then The word "cats" is not highlighted

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is opened
    And All fields are marked

    When I press "Alt-S"
    Then The word "cats" is highlighted

    When I click "Close" button
    And I click "Discard" button
    Then The Add window has closed
