# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from hamcrest import assert_that, equal_to
from lettuce import step

from xivo_acceptance.action.webi import ldap as ldap_action_webi
from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.action.webi import queue as queue_action_webi
from xivo_acceptance.helpers import context_helper, cti_helper, incall_helper
from xivo_lettuce import func, common


@step(u'Given the switchboard is configured for ldap lookup with location and department$')
def given_the_switchboard_is_configured_for_ldap_lookup_with_location_and_department(step):
    context_helper.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    step.given('Given the LDAP server is configured and active')
    ldap_action_webi.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass',
        display_name=['cn', 'st', 'o'])

    directory_action_webi.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber,st,o',
        '',
        {'name': 'cn',
         'number': 'telephoneNumber',
         'location': 'st',
         'department': 'o'}
    )
    directory_action_webi.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Location', '', '{db-location}'),
         ('Department', '', '{db-department}')]
    )
    directory_action_webi.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )


@step(u'Given the switchboard is configured for ldap lookup with location$')
def given_the_switchboard_is_configured_for_ldap_lookup_with_location(step):
    context_helper.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    step.given('Given the LDAP server is configured and active')
    ldap_action_webi.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    ldap_action_webi.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass',
        display_name=['cn', 'st'])

    directory_action_webi.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber,st',
        '',
        {'name': 'cn',
         'number': 'telephoneNumber',
         'location': 'st'}
    )
    directory_action_webi.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Location', '', '{db-location}')]
    )
    directory_action_webi.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )


@step(u'Given the switchboard is configured for ldap lookup$')
def given_the_switchboard_is_configured_for_ldap_lookup(step):
    context_helper.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    step.given('Given the LDAP server is configured and active')
    ldap_action_webi.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass')

    directory_action_webi.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber',
        '',
        {'name': 'cn',
         'number': 'telephoneNumber'}
    )
    directory_action_webi.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}')]
    )
    directory_action_webi.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )


@step(u'Given the switchboard is configured for internal directory lookup')
def given_the_switchboard_is_configured_for_internal_directory_lookup(step):
    context_helper.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    directory_action_webi.add_or_replace_directory(
        'xivodirswitchboard',
        'phonebook',
        'phonebook.firstname,phonebook.lastname,phonebook.displayname,phonebook.society,phonebooknumber.office.number',
        '',
        {'name': 'phonebook.displayname',
         'number': 'phonebooknumber.office.number',
         'mobile': 'phonebooknumber.mobile.number'}
    )
    directory_action_webi.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Number', 'number_mobile', '{db-mobile}')]
    )
    directory_action_webi.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['xivodirswitchboard']
    )


@step(u'Given the display filter "([^"]*)" exists with the following fields:')
def given_the_display_filter_group1_exists_with_the_following_fields(step, filter_name):
    field_list = []
    for line in step.hashes:
        field_list.append((line['Field title'], line['Field type'], line['Display format']))
    directory_action_webi.add_or_replace_display(filter_name, field_list)


@step(u'Given the user "([^"]*)" is configured for switchboard use')
def given_the_user_group1_is_configured_for_switchboard_use(step, user):
    user_action_webi.switchboard_config_for_user(user)


@step(u'Given there is a switchboard configured as:')
def given_there_is_a_switchboard_configured_as(step):
    for config in step.hashes:
        queue_action_webi.add_or_replace_switchboard_queue(
            config['incalls queue name'],
            config['incalls queue number'],
            config['incalls queue context'],
            config['agents'])

        queue_action_webi.add_or_replace_switchboard_hold_queue(
            config['hold calls queue name'],
            config['hold calls queue number'],
            config['hold calls queue context'])

        incall_helper.add_or_replace_incall(number=config['incalls queue number'],
                                            context='from-extern',
                                            dst_type='queue',
                                            dst_name=config['incalls queue name'])


@step(u'When I search a transfer destination "([^"]*)"')
def when_i_search_a_transfer_destination_1(step, search):
    cti_helper.set_search_for_directory(search)


@step(u'When the switchboard "([^"]*)" selects the incoming call from "([^"]*)" number "([^"]*)"')
def when_the_switchboard_1_selects_the_incoming_call_from_2_number_3(step, switchboard, cid_name, cid_num):
    common.wait_until(_switchboard_has_incoming_call, cid_name, cid_num, tries=10)
    cti_helper.switchboard_answer_incoming_call(cid_name, cid_num)


@step(u'When the switchboard "([^"]*)" hangs up')
def when_the_switchboard_group1_hangs_up(step, switchboard):
    cti_helper.switchboard_hang_up()


@step(u'Then the switchboard "([^"]*)" is not talking to anyone')
def then_the_switchboard_1_is_not_talking_to_anyone(step, switchboard):
    current_call = cti_helper.get_switchboard_current_call_infos()
    assert_that(current_call['caller_id'], equal_to(""))
    phone = step.scenario.phone_register.get_user_phone(switchboard)
    phone.is_hungup()


@step(u'Then the switchboard is talking to "([^"]*)" number "([^"]*)"')
def then_the_switchboard_is_talking_to_1_number_2(step, cid_name, cid_num):
    common.wait_until(_switchboard_has_current_call, tries=10)
    current_call = cti_helper.get_switchboard_current_call_infos()
    assert_that(current_call['caller_id'], equal_to("%s <%s>" % (cid_name, cid_num)))


@step(u'Then I see transfer destinations:')
def then_i_see_transfer_destinations(step):
    res = cti_helper.get_switchboard_infos()
    assert_res = func.has_subsets_of_dicts(step.hashes, res['return_value']['content'])
    assert_that(assert_res, equal_to(True))


@step(u'Then I see no transfer destinations')
def then_i_see_no_transfer_destinations(step):
    common.wait_until(_switchboard_has_no_transfer_destination, tries=3)


def _switchboard_has_incoming_call(cid_name, cid_num):
    incomings = cti_helper.get_switchboard_incoming_calls_infos()['incoming_calls']
    return [incoming for incoming in incomings
            if incoming['cid_name'] == cid_name
            and incoming['cid_num'] == cid_num]


def _switchboard_has_current_call():
    current_call = cti_helper.get_switchboard_current_call_infos()
    return current_call['caller_id'] != ""


def _switchboard_has_no_transfer_destination():
    res = cti_helper.get_switchboard_infos()
    return res['return_value']['content'] == []
