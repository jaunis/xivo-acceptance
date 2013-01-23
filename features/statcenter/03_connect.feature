Feature: Stat

    Scenario: Generation of event CONNECT
        Given there are no calls running
        Given there is no agents logged
        Given there is no "CONNECT" entry in queue "q03"
        Given there is a user "User" "003" with extension "1003@statscenter"
        Given there is a agent "Agent" "003" with extension "003@statscenter"
        Given there are queues with infos:
            | name | number | context     | agents_number |
            | q03  | 5003   | statscenter | 003           |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "003" on extension "1003@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I wait call then i answer then i hang up after "3s"
        Given there is 1 calls to extension "5003@statscenter" and wait
        Given I wait 10 seconds for the calls processing
        Then i should see 1 "CONNECT" event in queue "q03" in the queue log
