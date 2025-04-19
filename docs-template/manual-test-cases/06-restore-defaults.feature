#noinspection CucumberUndefinedStep
Feature: Restore defaults

  Background:
  Test "manual_test.py" was executed.
  Profile "CFH Manual Test 1" was opened.

  @smoke @browser
  Scenario: Use "Restore Defaults" button
    Given I opened Browser
    And I selected all notes
    And I opened "Highlight" dialog

    And I set "Highlight" dialog state:
      | Note Type     | "Basic"  |
      | Field         | "Back"   |
      | Exclude words | "the"    |
      | Format        | "Italic" |
      | Fields        | "Front"  |
    And I set "Highlight" dialog state:
      | Note Type     | "Cloze"      |
      | Field         | "Back Extra" |
      | Exclude words | "an"         |
      | Format        | "Underline"  |
      | Fields        | "Text"       |
    And I click "Cancel" button
    Then "Highlight" dialog has closed

    When I open "Highlight" dialog
    Then "Highlight" dialog has state:
      | Note Type     | "Cloze"      |
      | Field         | "Back Extra" |
      | Exclude words | "an"         |
      | Format        | "Underline"  |
      | Fields        | "Text"       |

    When I click "Restore Defaults" button
    Then "Highlight" dialog has state:
      | Note Type     | "Basic"   |
      | Field         | "Front"   |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I select "Cloze" Note Type
    Then "Highlight" dialog has state:
      | Note Type     | "Cloze"   |
      | Field         | "Text"    |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I click "Cancel" button
    Then "Highlight" dialog has closed
