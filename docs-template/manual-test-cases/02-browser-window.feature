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
    Then Collocations in "Back" field are highlighted in all notes
    And "Statistics" window was shown
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 12
      Notes processed: 12
      Notes modified: 12
      Fields processed: 12
      Fields modified: 12
      """

    When I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    And I clicked "Select All" button
    And I clicked "Start" button
    Then Collocations in "Back" field are NOT highlighted in all notes
    And "Statistics" window was shown
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 12
      Notes processed: 12
      Notes modified: 12
      Fields processed: 24
      Fields modified: 12
      """

    When I select all notes
    And I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is opened and it has all fields selected
    When I click "Cancel" button
    Then The "Highlight" dialog has closed

  @smoke @browser @editor
  Scenario: Highlight and erase a single note in Notes mode

    When I select one note in Browser
    And I click "Highlight" button
    Then The "Highlight" dialog is shown
    And All fields are selected

    When I click "Start" button
    Then Collocation in "Back" field was highlighted
    But "Statistics" windows was not shown

    When I click "Erase" button
    Then Collocation in "Back" field was NOT highlighted
    But "Statistics" windows was not shown

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is shown
    When I press "Alt-S"
    Then Collocation in "Back" field stays highlighted
    But "Statistics" windows was not shown

  @smoke @browser
  Scenario: Highlight and erase several notes in Cards mode

    Given I opened Browser
    And I switched Browser to Cards mode

    When I select all cards
    And I click context menu "Cross-Field Highlighter" -> "Highlight..."
    And I entered
      | Note Type     | "Cloze"             |
      | Field         | "Text"              |
      | Exclude words | "a an to"           |
      | Format        | "Yellow Background" |
      | Fields        | "Back Extra"        |
    And I clicked "Start" button
    Then Collocations in "Back" field are highlighted in all 2 Cloze cards
    And "Statistics" window was shown
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 1
      Notes processed: 1
      Notes modified: 1
      Fields processed: 1
      Fields modified: 1
      """

    When I select all cards
    And I click context menu "Cross-Field Highlighter" -> "Erase..."
    When I choose
      | Note Type | "Cloze"              |
      | Fields    | "Text", "Back Extra" |
    And I clicked "Start" button
    Then Collocations in "Back" field are NOT highlighted in all 2 Cloze cards
    And "Statistics" window was shown
      """
      Notes selected in Browser: 12
      Notes of type "Cloze": 1
      Notes processed: 1
      Notes modified: 1
      Fields processed: 2
      Fields modified: 1
      """
