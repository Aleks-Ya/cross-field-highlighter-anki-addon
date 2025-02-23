Feature: Study Editor

  Background:
  Profile "CFH Manual Test 1" was opened.
  Test notes were imported.
  The Main window is open.

  @smoke @editor @study
  Scenario: Highlight note edited during studying
    When I select "Default" deck
    And I click "Study Now" button
    And I click "Edit" button
    And I click "Highlight" button
    And I click "Select All" button
    And I click "Start" button
    Then The collocation in "Back" field is highlighted
    But "Statistics" windows was not shown

    When I click "Erase" button
    And I click "Select All" button
    And I click "Start" button
    Then Collocation in "Back" field was NOT highlighted
    But "Statistics" windows was not shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is shown
    When I press "Alt-S"
    Then Collocation in "Back" field are highlighted
    But "Statistics" windows was not shown
