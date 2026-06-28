#noinspection CucumberUndefinedStep
Feature: Switch Profile
  "Highlight" and "Erase" windows preferences should be saved when Note Type is changed in "Add" window.

  Background:
  I opened "Profiles" dialog.
  I executed "manual_tests_data.py".
  I opened "CFH Manual Test 1" profile.

  @smoke @add
  Scenario: "Highlight" dialog state is saved when Note Type is switched

    Given I opened "Add" window
    And I chose "Basic" note type

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

    When I open "Add" window
    And I chose "Basic" note type

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