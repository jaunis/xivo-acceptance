Feature: Line

    Scenario: Add a SIP line and remove it
        When I add a SIP line with infos:
        | context |
        | default |
        Then this line is displayed in the list
        When I remove this line
        Then this line is not displayed in the list

    # BUG #3642
    Scenario: See IPBX infos in line page with accent in callerid
        Given there is a user "André" "óíúéåäë" with extension "1801@default"
        When I edit the line "1801"
        When I go to the "IPBX Infos" tab
        Then I see in IPBX Infos tab value "callerid" has set to "André óíúéåäë" <1801>

    #Test X-325
    Scenario: Choose custom SIP codec
        When I add a SIP line with infos:
        | context | custom_codecs              |
        | default | Siren14 (G.722.1C) (Audio) |
        Then the codec "siren14" appears after typing 'sip show peer' in asterisk
        When I disable custom codecs for this line
        Then the codec "siren14" does not appear after typing 'sip show peer' in asterisk