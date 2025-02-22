Feature: Switch Profile
  "Highlight" and "Erase" windows preferences should be saved for each Profile individually.

  Background:
  Profile "CFH Manual Test 1" was opened.
  Test notes were imported to profile "CFH Manual Test 1".
  Profile "CFH Manual Test 2" exists.
  The Main window is opened for Profile "CFH Manual Test 1".

  @smoke @add @editor
  Scenario: "Highlight" dialog state is saved for each profile separately

    When I open "Add" window
    And I open "Highlight" dialog
    And I choose
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
    And I open "Highlight" dialog
    Then "Highlight" dialog has default settings
      | Note Type     | "Basic"   |
      | Field         | "Front"   |
      | Exclude words | "a an to" |
      | Format        | "Bold"    |
      | Fields        | -         |

    When I choose
      | Note Type     | "Basic"  |
      | Field         | "Front"  |
      | Exclude words | "an"     |
      | Format        | "Italic" |
      | Fields        | "Back"   |
    And I click "Cancel" button
    Then "Highlight" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 1" profile
    And I open "Highlight" dialog
    Then "Highlight" dialog has
      | Note Type     | "Basic"             |
      | Field         | "Back"              |
      | Exclude words | "the"               |
      | Format        | "Yellow Background" |
      | Fields        | "Front"             |

  @smoke @add @editor
  Scenario: "Erase" dialog state is saved for each profile separately

    When I open "Add" window
    And I open "Erase" dialog
    And I choose
      | Note Type | "Basic" |
      | Fields    | "Back"  |
    And I click "Cancel" button
    Then "Erase" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 2" profile
    And I open "Add" window
    And I open "Erase" dialog
    Then "Erase" dialog has default settings
      | Note Type | "Basic" |
      | Fields    | -       |

    When I choose
      | Note Type | "Basic" |
      | Fields    | "Front" |
    And I click "Cancel" button
    Then "Erase" dialog closes

    When I click menu "File" - "Switch Profile"
    And I open "CFH Manual Test 1" profile
    And I open "Erase" dialog
    Then "Erase" dialog has
      | Note Type | "Basic" |
      | Fields    | "Back"  |