Feature: Stat

    Scenario: Generation of event EXITWITHTIMEOUT
        Given there are no calls running
        Given there is no "EXITWITHTIMEOUT" entry in queue "q12"
        Given there is a user "User" "012" with extension "1012@statscenter"
        Given there is a agent "Agent" "012" with extension "012@statscenter"
        Given there is a queue "q12" with ringing time of "30s" with extension "5012@statscenter" with agent "012"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "012" on extension "1012@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 2 calls to extension "5012@statscenter" and wait
        Given I wait 35 seconds for the calls processing
        Then i should see 2 "EXITWITHTIMEOUT" event in queue "q12" in the queue log
