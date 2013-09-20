Feature: Provisioning with multiple SIP lines


    Scenario: multiline with func keys preconditions
        Given I have the following device templates:
            | id         | label       |
            | mytemplate | My Template |
        Given I have the following devices:
            | id       | ip       | mac               | model | vendor | version | plugin                |
            | myaastra | 10.0.0.1 | 00:11:22:33:44:55 | 6731i | Aastra | 3.2.2   | xivo-aastra-3.2.2-SP3 |
        Given I have the following users:
            | id | firstname | lastname |
            | 20 | Lion      | King     |
            | 21 | Simba     | King     |
        Given the user "Mufasa" has the following func keys:
            | key | type    | destination | label   | supervision |
            | 1   | DND     |             | dnd     | enabled     |
            | 2   | Parking | 700         | parking | disabled    |
        Given I have the following lines:
            | id | context | protocol | device_slot |
            | 30 | default | sip      | 1           |
        Given I have the following extensions:
            | id | context | exten |
            | 40 | default | 1000  |
        Given I have the following links:
            | user_id | line_id | extension_id |
            | 20      | 30      | 40           |
            | 21      | 30      | 40           |

    Scenario: Edit a device
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I update device "00:11:22:33:44:55" with the following parameters
            | template_id |
            | mytemplate  |
        When I synchronize device "00:11:22:33:44:55"
        Then the device "00:11:22:33:44:55" has the following parameters:
            | caller id | extension |
            | Mufasa | 1000      |
        Then my phone has the following func keys:
            | key | type    | destination | label   | supervision |
            | 1   | DND     |             | dnd     | enabled     |
            | 2   | Parking | 700         | parking | disabled    |
        Then device "00:11:22:33:44:55" can send and receive calls

    Scenario: Delete a device
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I delete device "00:11:22:33:44:55"
        When I synchronize device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" is in autoprov mode
        Then device "00:11:22:33:44:55" does not have any func keys
        Then "Mufasa" does not have any devices
        Then "Simba" does not have any devices

    Scenario: Associate a device to the main user
        Given all preconditions are ready
        When I associate "Mufasa" with device "00:11:22:33:44:55"
        When I synchronize device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" has the following parameters:
            | caller id | extension |
            | Mufasa | 1000      |
        Then device "00:11:22:33:44:55" has the following func keys:
            | key | type    | destination | label   | supervision |
            | 1   | DND     |             | dnd     | enabled     |
            | 2   | Parking | 700         | parking | disabled    |
        Then "Mufasa" is associated to the device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" can send and receive calls

    Scenario: Update the device of a secondary user
        Given all preconditions are ready
        When I edit user "Simba"
        Then I cannot modify the line

    Scenario: Deassociate a device from the main user
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I remove the device used by "Mufasa"
        When I synchronize device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" is in autoprov mode
        Then device "00:11:22:33:44:55" does not have any func keys
        Then "Mufasa" no longer has any devices
        Then "Simba" no longer has any devices

    Scenario: Associate another device to the main user
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        Given I have the following devices:
            | id           | ip       | mac               | model | vendor | version | plugin                |
            | secondaastra | 10.0.0.2 | 00:11:22:33:44:56 | 6731i | Aastra | 3.2.2   | xivo-aastra-3.2.2-SP3 |
        When I associate "Mufasa" with device "00:11:22:33:44:56"
        When I synchronize device "00:11:22:33:44:55"
        When I synchronize device "00:11:22:33:44:56"

        Then device "00:11:22:33:44:55" is in autoprov mode
        Then device "00:11:22:33:44:55" does not have any func keys

        Then device "00:11:22:33:44:56" has the following parameters:
            | caller id | extension |
            | Mufasa | 1000      |
        Then device "00:11:22:33:44:56" has the following func keys:
            | key | type    | destination | label   | supervision |
            | 1   | DND     |             | dnd     | enabled     |
            | 2   | Parking | 700         | parking | disabled    |
        Then device "00:11:22:33:44:56" can send and receive calls

    Scenario: Synchronize a device after updating the main user
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I update "Mufasa" with the following parameters:
            | caller id    | extension |
            | Supreme Lion | 1001      |
        When I add the following fuck keys to "Mufasa"
            | key | type       | destination | label  | supervision |
            | 3   | Customized | 1000        | custom | enabled     |
        When I synchronize device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" has the following parameters:
            | caller id | extension |
            | Mufasa | 1001      |
        Then device "00:11:22:33:44:55" has the following func keys:
            | key | type       | destination | label   | supervision |
            | 1   | DND        |             | dnd     | enabled     |
            | 2   | Parking    | 700         | parking | disabled    |
            | 3   | Customized | 1000        | custom  | enabled     |
        Then device "00:11:22:33:44:55" can send and receive calls

    Scenario: Reset to autoprov
        Given all preconditions are ready
        Given the device "00:11:22:33:44:55" is provisioned with the line "30"
        When I reset the device "00:11:22:33:44:55" to autoprov
        Then the device with mac "00:11:22:33:44:55" is in autoprov mode
        Then the device with mac "00:11:22:33:44:55" does not have any func keys
        Then the user "20" no longer has any devices
        Then the user "21" no longer has any devices

    Scenario: Deleting a line
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I delete the line used by "Mufasa"
        Then device with mac "00:11:22:33:44:55" is in autoprov mode
        Then "Mufasa" no longer has any devices
        Then "Simba" no longer has any devices

    Scenario: Reset to autoprov with guest code
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I dial "*guest" on device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" is in autoprov mode
        Then "Mufasa" no longer has any devices
        Then "Simba" no longer has any devices

    Scenario: Synchronizing a device with High Availability
        Given the server is configured for High Availability
        Given all preconditions are ready
        Given "Mufasa" has provisionned the device "00:11:22:33:44:55" with line "30"
        When I synchronize device "00:11:22:33:44:55"
        Then device "00:11:22:33:44:55" has the following parameters:
            | caller id | extension |
            | Mufasa | 1000      |
        Then device "00:11:22:33:44:55" has the following func keys:
            | key | type       | destination | label   | supervision |
            | 1   | DND        |             | dnd     | enabled     |
            | 2   | Parking    | 700         | parking | disabled    |
        Then device "00:11:22:33:44:55" is configured with 2 servers
        Then device "00:11:22:33:44:55" can send and receive calls
