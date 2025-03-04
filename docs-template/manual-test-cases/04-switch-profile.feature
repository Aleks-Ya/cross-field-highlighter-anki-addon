Feature: Switch Profile
  "Highlight" and "Erase" windows preferences should be saved for each Profile individually.

  Background:
  Profiles "CFH Manual Test 1" and "CFH Manual Test 2" were removed from Storage.
  Profile "CFH Manual Test 1" was opened.
  Test notes were imported to profile "CFH Manual Test 1".
  Profile "CFH Manual Test 2" exists.
  The Main window is opened for Profile "CFH Manual Test 1".

  @smoke @add
  Scenario: "Highlight" dialog state is saved for each profile separately

    When I open "Add" window
    And I choose "Basic" note type
    And I open "Highlight" dialog
    And I set state:
      | Note Type     | "Basic"             |
      | Field         | "Back"              |
      | Exclude words | "the"               |
      | Format        | "Yellow Background" |
      | Fields        | "Front"             |
    And I click "Cancel" button
    Then "Highlight" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 2" profile
    And I open "Add" window
    And I choose "Basic" note type
    And I open "Highlight" dialog
    Then "Highlight" dialog has default state:
      | Note Type     | "Basic"   |
      | Field         | "Front"   |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I set state:
      | Note Type     | "Basic"  |
      | Field         | "Front"  |
      | Exclude words | "an"     |
      | Format        | "Italic" |
      | Fields        | "Back"   |
    And I click "Cancel" button
    Then "Highlight" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 1" profile
    And I open "Add" window
    And I choose "Basic" note type
    And I open "Highlight" dialog
    Then "Highlight" dialog has state:
      | Note Type     | "Basic"             |
      | Field         | "Back"              |
      | Exclude words | "the"               |
      | Format        | "Yellow Background" |
      | Fields        | "Front"             |

  @smoke @add
  Scenario: "Erase" dialog state is saved for each profile separately

    When I open "Add" window
    And I choose "Basic" note type
    And I open "Erase" dialog
    And I set state:
      | Note Type | "Basic" |
      | Fields    | "Back"  |
    And I click "Cancel" button
    Then "Erase" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 2" profile
    And I open "Add" window
    And I choose "Basic" note type
    And I open "Erase" dialog
    Then "Erase" dialog has default state:
      | Note Type | "Basic" |
      | Fields    | -       |

    When I set state:
      | Note Type | "Basic" |
      | Fields    | "Front" |
    And I click "Cancel" button
    Then "Erase" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 1" profile
    And I open "Add" window
    And I choose "Basic" note type
    And I open "Erase" dialog
    Then "Erase" dialog has state:
      | Note Type | "Basic" |
      | Fields    | "Back"  |