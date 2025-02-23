Feature: Performance of highlight and erase operations

  @smoke @performance @browser
  Scenario: Highlight many notes
    Given the browser is open

    When I select 1 note
    And I click the Highlight button
    And I select another settings
    And I click the Cancel button

    Then the word `cats` is highlighted
