Feature: IAX general parameters

    Scenario: Enable shrink Caller ID
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Advanced"
        Given the option "Shrink CallerID" is not checked
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        When I check this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        Then this option is checked

    Scenario: Disable shrink Caller ID
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Advanced"
        Given the option "Shrink CallerID" is checked
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        When I uncheck this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Advanced"
        Then this option is not checked

    Scenario: Enable SRV lookup
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Default"
        Given the option "SRV lookup" is checked
        When I go on the General Settings > IAX Protocol page, tab "Default"
        When I check this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Default"
        Then this option is checked

    Scenario: Disable SRV lookup
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Default"
        Given the option "SRV lookup" is checked
        When I go on the General Settings > IAX Protocol page, tab "Default"
        When I uncheck this option
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Default"
        Then this option is not checked

    Scenario: Add a call limit
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Call limits"
        Given I don't see any call limit to "10.0.0.1" netmask "255.255.255.255"
        When I go on the General Settings > IAX Protocol page, tab "Call limits"
        When I add a call limit
        When I set the destination to "10.0.0.1"
        When I submit with errors
        Then I get errors
        When I go on the General Settings > IAX Protocol page, tab "Call limits"
        When I add a call limit
        When I set the destination to "10.0.0.1"
        When I set the netmask to "255.255.255.255"
        When I set the call limit to "1"
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Call limits"
        Then I see a call limit to "10.0.0.1" netmask "255.255.255.255" of "1" calls

    Scenario: Remove a call limit
        Given I am logged in
        Given I go on the General Settings > IAX Protocol page, tab "Call limits"
        Given I see a call limit to "10.0.0.1" netmask "255.255.255.255" of "1" calls
        When I go on the General Settings > IAX Protocol page, tab "Call limits"
        When I remove the call limits to "10.0.0.1" netmask "255.255.255.255"
        When I submit
        When I go on the General Settings > IAX Protocol page, tab "Call limits"
        Then I don't see a call limit to "10.0.0.1" netmask "255.255.255.255"