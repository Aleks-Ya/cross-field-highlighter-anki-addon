Feature: Highlight in Add Note window

  @smoke @add @editor
  Scenario: Highlight and erase operations in Add Note window

    Given I opened the Add Note window
    And I entered `cat` in "Front" field
    And I entered `cats` in "Back" field

    When I click "Highlight" button
    And I click "Select All" button
    And I click "Start" button
    Then The word `cats` is highlighted

    When I click "Erase" button
    And I click "Select All" button
    And I click "Start" button
    Then The word "cats" is not highlighted

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is opened and it has all fields selected

    When I press "Alt-S"
    Then The word "cats" is highlighted

    When I click "Close" button
    And I click "Discard" button
    Then The "Add" windows has closed
