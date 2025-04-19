#noinspection CucumberUndefinedStep
Feature: Performance of highlight and erase operations

  Background:
  Profile "CFH Manual Test 3 Big" was created by "manual_test.py".
  Profile "CFH Manual Test 3 Big" was opened.

  @smoke @performance @browser
  Scenario: Highlight many notes
    Given the browser is open

    When I select all notes
    And I click the Highlight button
    And I set state:
      | Note Type     | "Basic"             |
      | Field         | "Front"             |
      | Exclude words | "a an to"           |
      | Format        | "Yellow Background" |
      | Fields        | "Back"              |
    And I click the Start button
    Then The progress dialog is displayed
