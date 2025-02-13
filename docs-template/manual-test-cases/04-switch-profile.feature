Feature: Switch Profile

  Background:
  Profile "CFH Manual Test 1" was opened.
  Test notes were imported to profile "CFH Manual Test 1".
  Profile "CFH Manual Test 2" exists.
  The Main window is open.

  @smoke @browser @editor
  Scenario: Switch profile

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 2" profile
    And I click "Highlight" button
    Then The "Highlight" dialog has default settings

    When I select only "Back" field
    And I click "Start" button
    Then The collocation in "Back" field is highlighted

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 1" profile
    And I click "Highlight" button
    Then The "Highlight" dialog has all fields selected
