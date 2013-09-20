Feature: Provd

    Scenario: Update device config inherited of base config
        Given I only have the following users:
            | id | firstname | lastname  |
            | 1  | Greg      | Sanderson |
        Given I only have the following lines:
            | id | context | protocol | username | secret | device_slot |
            | 10 | default | sip      | toto     | tata   | 1           |
        Given I only have the following extensions:
            | id  | context | exten |
            | 100 | default | 1000  |
        Given I only have the following devices:
            | id | ip       | mac               |
            | 20 | 10.0.0.1 | 00:00:00:00:00:00 |
        When I create the following links:
            | user_id | line_id | extension_id |
            | 1       | 10      | 100          |
        Then I get a response with status "201"
        
        When I provision my device with my line_id "10" and ip "10.0.0.1"
        Then the device "20" has been provisioned with a configuration:
            | display_name   | number | username | auth_username | password |
            | Greg Sanderson | 1000   | toto     | toto          | tata     |
        
        When I edit the device "20" with infos:
            | vlan_enabled |
            | 0            |
        Then the device "20" has a config with the following parameters:
            | vlan_enabled |
            | 0            |
        
        When I edit the device "20" with infos:
            | vlan_enabled |
            |              |
        Then the device "20" has no config with the following keys:
            | keys         |
            | vlan_enabled |
