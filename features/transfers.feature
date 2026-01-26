Feature: Wypłata gotówki z bankomatu

  Scenario: Udana wypłata gotówki
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Nowak", pesel: "12345678901"
    And I perform "incoming" transfer with amount: "500" for account with pesel: "12345678901"
    When I perform "outgoing" transfer with amount: "100" for account with pesel: "12345678901"
    Then The transfer is successful
    And Account with pesel "12345678901" has "balance" equal to "400"

  Scenario: Niewystarczające środki na koncie
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Nowak", pesel: "12345678901"
    And I perform "incoming" transfer with amount: "50" for account with pesel: "12345678901"
    When I perform "outgoing" transfer with amount: "100" for account with pesel: "12345678901"
    Then The transfer fails with status "422"
    And Account with pesel "12345678901" has "balance" equal to "50"