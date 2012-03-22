Feature: Files

    Scenario: Add a long file name
        Given I am logged in
        Given a recording file with name "a.wav"
        Given a recording file with name "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.wav"
        Given a recording file with name "rec-1316188241-166453-sip-lasotel-in-23-000158c6-out.wav.wav"
        Then recording file "a.wav" is displayed in the list
        Then recording file "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.wav" is displayed in the list
        Then recording file "rec-1316188241-166453-sip-lasotel-in-23-000158c6-out.wav.wav" is displayed in the list