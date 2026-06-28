#noinspection CucumberUndefinedStep
Feature: Highlight in Add Note window

  Background:
  I opened "Profiles" dialog.
  I executed "manual_tests_data.py".
  I opened "CFH Manual Test 1" profile.

  @smoke @add
  Scenario: Use "Restore Defaults" button in "Highlight" dialog
    When I opened Browser
    And I selected all notes
    And I opened "Highlight" dialog
    Then "Highlight" dialog has default state:
      | Note Type     | "Basic"   |
      | Field         | "Front"   |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I set state:
      | Note Type     | "Cloze"      |
      | Field         | "Back Extra" |
      | Exclude words | "the"        |
      | Format        | "Italic"     |
      | Fields        | "Text"       |
    And I click "Restore Defaults" button
    Then "Highlight" dialog returns to default state:
      | Note Type     | "Basic"   |
      | Field         | "Front"   |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

  @smoke @add
  Scenario: Use "Restore Defaults" button in "Erase" dialog
    When I opened Browser
    And I selected all notes
    And I opened "Erase" dialog
    Then "Erase" dialog has default state:
      | Note Type | "Basic" |
      | Fields    | -       |

    When I set state:
      | Note Type | "Cloze"      |
      | Fields    | "Back Extra" |
    And I click "Restore Defaults" button
    Then "Erase" dialog returns to default state:
      | Note Type | "Basic" |
      | Fields    | -       |