Feature: Highlight Notes in Browser

  Background:
  Profile "CFH Manual Test 1" was opened.
  Test notes were imported from `cfh-test-profile-1.txt`.
  The Browser is opened in Notes mode.

  @smoke @browser
  Scenario: Highlight and erase several notes selected Note mode

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Highlight..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 11
      Notes processed: 11
      Notes modified: 11
      Fields processed: 11
      Fields modified: 11
      """
    And Collocations in "Back" field are highlighted in all notes

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 11
      Notes processed: 11
      Notes modified: 11
      Fields processed: 22
      Fields modified: 11
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
    But "Statistics" windows was not shown

    When I click "Erase" button
    Then The "Erase" dialog is shown
    And All fields are selected

    When I click "Start" button
    Then Collocation in "Back" field was NOT highlighted
    But "Statistics" windows was not shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is shown
    When I press "Alt-S"
    Then Collocation in "Back" field stays highlighted
    But "Statistics" windows was not shown

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
      Notes selected in Browser: 12
      Notes of type "Cloze": 1
      Notes processed: 1
      Notes modified: 1
      Fields processed: 1
      Fields modified: 1
      """
    And Collocations in "Back" field are highlighted in all 2 Cloze cards

    When I select all cards
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    When I set state:
      | Note Type | "Cloze"              |
      | Fields    | "Text", "Back Extra" |
    And I clicked "Start" button
    Then "Statistics" window was shown:
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 1
      Notes processed: 1
      Notes modified: 1
      Fields processed: 2
      Fields modified: 1
      """
    And Collocations in "Back" field are NOT highlighted in all 2 Cloze cards
