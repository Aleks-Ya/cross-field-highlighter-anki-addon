#noinspection CucumberUndefinedStep
Feature: Switch Profile
  "Highlight" and "Erase" windows preferences should be saved when Note Type is changed in "Add" window.

  Background:
  Test "manual_test.py" was executed.
  Profile "CFH Manual Test 1" was opened.

  @smoke @add
  Scenario: "Highlight" dialog state is saved when Note Type is switched

    Given Profile "CFH Manual Test 1" was removed from Storage
    And "Add" window is opened
    And "Basic" note type is chosen

    When I open "Highlight" dialog
    Then "Highlight" dialog has default state:
      | Note Type     | "Basic"   |
      | Field         | "Front"   |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I set state:
      | Note Type     | "Basic"             |
      | Field         | "Back"              |
      | Exclude words | "the"               |
      | Format        | "Yellow Background" |
      | Fields        | "Front"             |
    And I click "Cancel" button
    Then "Highlight" dialog closes

    When I choose "Cloze" note type
    And I open "Highlight" dialog
    Then "Highlight" dialog has default state:
      | Note Type     | "Cloze"   |
      | Field         | "Text"    |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I set state:
      | Note Type     | "Cloze"      |
      | Field         | "Back Extra" |
      | Exclude words | "an"         |
      | Format        | "Underline"  |
      | Fields        | "Text"       |
    And I click "Cancel" button
    Then "Highlight" dialog closes

    When I choose "Basic" note type
    And I open "Highlight" dialog
    Then "Highlight" dialog has state:
      | Note Type     | "Basic"             |
      | Field         | "Back"              |
      | Exclude words | "the"               |
      | Format        | "Yellow Background" |
      | Fields        | "Front"             |

    When I click "Cancel" button
    Then "Highlight" dialog closes

    And I choose "Cloze" note type
    And I open "Highlight" dialog
    Then "Highlight" dialog has state:
      | Note Type     | "Cloze"      |
      | Field         | "Back Extra" |
      | Exclude words | "an"         |
      | Format        | "Underline"  |
      | Fields        | "Text"       |

    When I click "Cancel" button
    Then "Highlight" dialog closes

  @smoke @add
  Scenario: "Erase" dialog state is saved when Note Type is switched

    Given "Add" window is opened
    And "Basic" note type is chosen

    When I open "Erase" dialog
    Then "Erase" dialog has default state:
      | Note Type | "Basic" |
      | Fields    | -       |

    When I set state:
      | Note Type | "Basic" |
      | Fields    | "Back"  |
    And I click "Cancel" button
    Then "Erase" dialog closes

    When I choose "Cloze" note type
    And I open "Erase" dialog
    Then "Erase" dialog has default state:
      | Note Type | "Cloze" |
      | Fields    | -       |

    When I set state:
      | Note Type | "Cloze"      |
      | Fields    | "Back Extra" |
    And I click "Cancel" button
    Then "Erase" dialog closes

    When I choose "Basic" note type
    And I open "Erase" dialog
    Then "Erase" dialog has state:
      | Note Type | "Basic" |
      | Fields    | "Back"  |

    When I click "Cancel" button
    Then "Erase" dialog closes

    And I choose "Cloze" note type
    And I open "Erase" dialog
    Then "Erase" dialog has state:
      | Note Type | "Cloze"      |
      | Fields    | "Back Extra" |

    When I click "Cancel" button
    Then "Erase" dialog closes