Feature: Highlight Notes in Browser

  Background:
  Profile "CFH Manual Test 1" was opened.
  Test notes were imported from `cfh-test-profile-1.txt`.
  The Browser is opened.

  @smoke @browser
  Scenario: Highlight several notes selected in Browser

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Highlight..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then Collocations in "Back" field are highlighted in all notes
    And "Statistics" window was shown

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then Collocations in "Back" field are NOT highlighted in all notes
    And "Statistics" window was shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is opened and it has all fields selected
    When I click "Cancel" button
    Then The "Highlight" dialog has closed

  @smoke @browser @editor
  Scenario: Highlight a note in the browser

    When I select one note in Browser
    And I click "Highlight" button
    Then The "Highlight" dialog is shown
    And All fields are selected

    When I click "Start" button
    Then Collocation in "Back" field was highlighted
    But "Statistics" windows was not shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is shown
    When I press "Alt-S"
    Then Collocation in "Back" field stays highlighted
    But "Statistics" windows was not shown

    When I click "Erase" button
    Then Collocation in "Back" field was NOT highlighted
    But "Statistics" windows was not shown
