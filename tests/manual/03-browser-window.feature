#noinspection CucumberUndefinedStep
Feature: Highlight Notes in Browser

  Background:
  I opened "Profiles" dialog.
  I executed "manual_tests_data.py".
  I opened "CFH Manual Test 1" profile.
  The Browser is opened in Notes mode.

  @smoke @browser
  Scenario: Highlight and erase several notes selected Note mode

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Highlight..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 49
      Notes of type "Cloze": 48
      Notes processed: 48
      Notes modified: 45
      Fields processed: 48
      Fields modified: 45
      """
    And Collocations in "Back" field are highlighted in all notes

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 49
      Notes of type "Cloze": 48
      Notes processed: 48
      Notes modified: 45
      Fields processed: 96
      Fields modified: 45
      """
    And Collocations in "Back" field are NOT highlighted in all notes

    When I select all notes
    And I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is opened and it has all fields selected
    When I press "Alt-C"
    Then The "Highlight" dialog has closed

  @smoke @browser @editor
  Scenario: Highlight and erase a single note in Notes mode
    Given One note is selected in Browser

    When I click "Highlight" button
    Then The "Highlight" dialog is shown
    And All fields are selected

    When I click "Start" button
    Then Collocation in "Back" field was highlighted
    But "Statistics" windows was NOT shown

    When I click "Erase" button
    Then The "Erase" dialog is shown
    And All fields are selected

    When I click "Start" button
    Then Collocation in "Back" field was NOT highlighted
    But "Statistics" windows was NOT shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is shown
    When I press "Alt-S"
    Then Collocation in "Back" field is highlighted
    But "Statistics" windows was NOT shown

  @smoke @browser
  Scenario: Highlight and erase several notes in Cards mode
    Given Browser is opened in Cards mode

    When I select all cards
    And I click context menu "Cross-Field Highlighter" -> "Highlight..."
    And I set state:
      | Note Type     | "Cloze"             |
      | Field         | "Text"              |
      | Exclude words | "a an to"           |
      | Format        | "Yellow Background" |
      | Fields        | "Back Extra"        |
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 49
      Notes of type "Cloze": 1
      Notes processed: 1
      Notes modified: 1
      Fields processed: 1
      Fields modified: 1
      """
    And Collocation in "Back Extra" field is highlighted in the Cloze card

    When I select all cards
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    When I set state:
      | Note Type | "Cloze"              |
      | Fields    | "Text", "Back Extra" |
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 49
      Notes of type "Cloze": 1
      Notes processed: 1
      Notes modified: 1
      Fields processed: 2
      Fields modified: 1
      """
    And Collocation in "Back Extra" field is NOT highlighted in the Cloze card
