#noinspection CucumberUndefinedStep
Feature: Study Editor

  Background:
  I opened "Profiles" dialog.
  I executed "manual_tests_data.py".
  I opened "CFH Manual Test 1" profile.
  The Main window is open.

  @smoke @editor @study
  Scenario: Highlight note edited during studying
    When I select "Default" deck
    And I click "Study Now" button
    And I click "Edit" button
    And The Study Editor is opened
    And I click "Highlight" button
    And I click "Select All" button
    And I click "Start" button
    Then Collocation in "Back" field is highlighted
    But "Statistics" windows was NOT shown

    When I click "Erase" button
    And I click "Select All" button
    And I click "Start" button
    Then Collocation in "Back" field is NOT highlighted
    But "Statistics" windows was NOT shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is shown
    When I press "Alt-S"
    Then Collocation in "Back" field is highlighted
    But "Statistics" windows was NOT shown

    When I click "Close" button
    Then The Study Editor has closed