#noinspection CucumberUndefinedStep
Feature: Performance of highlight and erase operations

  Background:
  I opened "Profiles" dialog.
  I executed "manual_tests_data.py".
  Profile "CFH Manual Test 3 Big" was opened.

  @smoke @performance @browser
  Scenario: Highlight many notes
    When I open Browser
    And I select all notes
    And I click context menu "Cross-Field Highlighter" -> "Highlight..."
    And I set state:
      | Note Type     | "Basic"             |
      | Field         | "Front"             |
      | Exclude words | "a an to"           |
      | Format        | "Yellow Background" |
      | Fields        | "Back"              |
    And I click the Start button
    Then The progress dialog is displayed
