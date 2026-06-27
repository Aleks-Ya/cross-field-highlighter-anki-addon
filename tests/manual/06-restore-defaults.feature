#noinspection CucumberUndefinedStep
Feature: Highlight in Add Note window

  Background:
  I executed "manual_test.py".
  Profile "CFH Manual Test 1" was opened.

  @smoke @add
  Scenario: Use "Restore Defaults" button
    Given I opened Browser
    And I selected all notes
    And I opened "Highlight" dialog

    And I selected "Basic" Note Type
    And I selected "Front" field
    And I typed "the" in "Exclude words" field
    And I selected "Italic" format
    And I marked "Back" field

    And I selected "Basic" Note Type
    And I selected "Front" field
    And I typed "the" in "Exclude words" field
    And I selected "Italic" format
    And I marked "Back" field

    And I click "Start" button
    Then The word "cats" is highlighted

    When I click "Erase" button
    And I click "Select All" button
    And I click "Start" button
    Then The word "cats" is not highlighted

    When I press "Ctrl-Shift-H"
    Then The "Highlight" dialog is opened
    And All fields are marked

    When I press "Alt-S"
    Then The word "cats" is highlighted

    When I click "Close" button
    And I click "Discard" button
    Then The Add window has closed
