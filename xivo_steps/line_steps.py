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

import time
import re

from hamcrest import *
from lettuce import step, world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from xivo_acceptance.action.restapi import line_action_restapi, \
    line_sip_action_restapi
from xivo_acceptance.action.webi import line as line_action_webi
from xivo_acceptance.helpers import line_helper, line_sip_helper, context_helper
from xivo_lettuce import common, form
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.widget.codec import CodecWidget


@step(u'Given there are no custom lines with interface beginning with "([^"]*)"')
def given_there_are_no_custom_lines_with_interface_beginning_with_1(step, interface_start):
    common.remove_element_if_exist('line', interface_start)


@step(u'Given I set the following options in line "([^"]*)":')
def given_i_set_the_following_options_in_line_1(step, line_number):
    line_id = line_helper.find_line_id_with_exten_context(line_number, 'default')
    common.open_url('line', 'edit', {'id': line_id})

    for line_data in step.hashes:
        for key, value in line_data.iteritems():
            if key == 'NAT':
                common.go_to_tab('General')
                form.select.set_select_field_with_label('NAT', value)
            elif key == 'IP addressing type':
                common.go_to_tab('Advanced')
                form.select.set_select_field_with_label('IP Addressing type', value)
            elif key == 'IP address':
                common.go_to_tab('Advanced')
                form.select.set_select_field_with_label('IP Addressing type', 'Static')
                form.input.set_text_field_with_label('IP address', value)
            else:
                raise Exception('%s is not a valid key' % key)

    form.submit.submit_form()


@step(u'Given the line "([^"]*)" has the codec "([^"]*)"')
def given_the_line_group1_has_the_codec_group2(step, linenumber, codec):
    _add_codec_to_line(codec, linenumber)


@step(u'Given the line "(\d+)@(\w+)" is disabled')
def given_the_line_group1_is_disabled(step, extension, context):
    common.open_url('line')
    _search_for_line(extension, context)
    _click_checkbox_for_line(extension)
    _disable_selected_lines()
    time.sleep(world.timeout)  # wait for dialplan to finish reloading


def _search_for_line(extension, context):
    form.input.edit_text_field_with_id('it-toolbar-search', extension)
    form.select.set_select_field_with_id('it-toolbar-context', context)


def _click_checkbox_for_line(extension):
    line_element = common.get_line(extension)
    checkbox = line_element.find_element_by_css_selector(".it-checkbox")
    checkbox.click()


def _disable_selected_lines():
    menu_button = world.browser.find_element_by_id("toolbar-bt-advanced")
    ActionChains(world.browser).move_to_element(menu_button).perform()

    disable_button = world.browser.find_element_by_id("toolbar-advanced-menu-disable")
    ActionChains(world.browser).click(disable_button).perform()


@step(u'Given I have the following lines:')
def given_i_have_the_following_lines(step):
    for lineinfo in step.hashes:
        _delete_line(lineinfo)
        _create_line(lineinfo)


@step(u'Given I have no line with id "([^"]*)"')
def given_i_have_no_line_with_id_group1(step, line_id):
    line_id = int(line_id)
    line_helper.delete_line(line_id)


def _delete_line(lineinfo):
    if 'id' in lineinfo:
        line_helper.delete_line(int(lineinfo['id']))
    if 'username' in lineinfo:
        lines = line_helper.find_with_name(lineinfo['username'])
        for line in lines:
            line_helper.delete_line(line.id)


def _create_line(lineinfo):
    protocol = lineinfo['protocol'].lower()
    if protocol == 'sip':
        line_sip_helper.create_line_sip(lineinfo)
    else:
        line_helper.create(lineinfo)


@step(u'Given I have an internal context named "([^"]*)"')
def given_i_have_an_internal_context_named_group1(step, context):
    context_helper.create_context(context)


@step(u'When I ask for the line_sip with id "([^"]*)"')
def when_i_ask_for_the_line_sip_with_id_group1(step, lineid):
    world.response = line_sip_action_restapi.get(lineid)


@step(u'When I create an empty SIP line$')
def when_i_create_an_empty_line(step):
    world.response = line_sip_action_restapi.create_line_sip({})


@step(u'When I create a line_sip with the following parameters:')
def when_i_create_a_line_with_the_following_parameters(step):
    parameters = _extract_line_parameters(step)
    world.response = line_sip_action_restapi.create_line_sip(parameters)


@step(u'When I update the line_sip with id "([^"]*)" using the following parameters:')
def when_i_update_the_user_with_id_group1_using_the_following_parameters(step, lineid):
    lineinfo = _extract_line_parameters(step)
    world.response = line_sip_action_restapi.update(lineid, lineinfo)


@step(u'When I delete line sip "([^"]*)"')
def when_i_delete_line_group1(step, line_id):
    world.response = line_sip_action_restapi.delete(line_id)


@step(u'When I customize line "([^"]*)" codecs to:')
def when_i_customize_line_codecs_to(step, number):
    codecs = (entry['codec'] for entry in step.hashes)
    _add_codec_list_to_line(codecs, number)


@step(u'When I disable line codecs customization for line "([^"]*)"')
def when_i_disable_line_codecs_customization_for_line(step, number):
    line_id = line_helper.find_line_id_with_exten_context(number, 'default')
    common.open_url('line', 'edit', {'id': line_id})
    _open_codec_page()
    Checkbox.from_label("Customize codecs:").uncheck()
    form.submit.submit_form()


@step(u'When I add a SIP line with infos:')
def when_i_add_a_sip_line_with_infos(step):
    for line_infos in step.hashes:
        common.open_url('line', 'add', {'proto': 'sip'})
        world.id = _get_line_name()
        if 'context' in line_infos:
            context = line_infos['context']
            form.select.set_select_field_with_id_containing('it-protocol-context', context)
        if 'custom_codecs' in line_infos:
            codec = line_infos['custom_codecs']
            _add_custom_codec(codec)
        form.submit.submit_form()


def _get_line_name():
    return world.browser.find_element_by_id('it-protocol-name').get_attribute('value')


def _add_custom_codec(codec):
    _open_codec_page()
    codec_widget = CodecWidget()
    codec_widget.add(codec)


@step(u'When I add a custom line with infos:')
def when_i_add_a_custom_line(step):
    for line in step.hashes:
        common.open_url('line', 'add', {'proto': 'custom'})
        if 'interface' in line:
            form.input.set_text_field_with_id('it-protocol-interface', line['interface'])
            form.submit.submit_form()


@step(u'When I add the codec "([^"]*)" to the line with number "([^"]*)"')
def when_i_add_the_custom_codec_to_the_line_with_number(step, codec, linenumber):
    _add_codec_to_line(codec, linenumber)


@step(u'When I disable custom codecs for this line')
def when_i_disable_custom_codecs_for_this_line(step):
    line_action_webi.search_line_number(world.id)
    common.edit_line(world.id)
    _open_codec_page()
    Checkbox.from_label("Customize codecs:").uncheck()
    form.submit.submit_form()


@step(u'When I remove this line')
def when_i_remove_this_line(step):
    common.open_url('line', 'search', {'search': world.id})
    common.remove_line(world.id)
    common.open_url('line', 'search', {'search': ''})


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    line_id = line_helper.find_line_id_with_exten_context(linenumber, 'default')
    common.open_url('line', 'edit', {'id': line_id})


@step(u'When I remove the codec "([^"]*)" from the line with number "([^"]*)"')
def when_i_remove_the_codec_from_the_line_with_number(step, codec, linenumber):
    line_id = line_helper.find_line_id_with_exten_context(linenumber, 'default')
    common.open_url('line', 'edit', {'id': line_id})
    _open_codec_page()
    codec_widget = CodecWidget()
    codec_widget.remove(codec)
    form.submit.submit_form()


@step(u'When I ask for the list of lines$')
def when_i_ask_for_the_list_of_lines(step):
    world.response = line_action_restapi.all_lines()


@step(u'When I ask for line with id "([^"]*)"')
def when_i_ask_for_line_with_id_group1(step, line_id):
    line_id = int(line_id)
    world.response = line_action_restapi.get(line_id)


@step(u'Then I see a line with infos:')
def then_i_see_a_line_with_infos(step):
    expected_line = step.hashes[0]
    if 'device' in expected_line:
        expected_line['device'] = True if expected_line['device'] == 'True' else False
    number = expected_line['number']
    common.open_url('line', 'search', {'search': number})
    actual_line = line_action_webi.get_line_list_entry(number)
    assert_that(actual_line, has_entries(expected_line))
    common.open_url('user', 'search', {'search': ''})


@step(u'Then the line with number "([^"]*)" does not have the codec "([^"]*)"')
def then_the_line_with_number_group1_does_not_have_the_codec_group2(step, linenumber, codec):
    line = line_helper.find_with_exten_context(linenumber, 'default')
    sip_peer = line.name
    assert not check_codec_for_sip_line(sip_peer, codec)


def check_codec_for_sip_line(peer, codec):
    command = ['asterisk', '-rx', '"sip show peer %s"' % peer]
    output = world.ssh_client_xivo.out_call(command)
    codec_line = [x for x in output.split("\n") if 'Codecs' in x][0]
    codec_list = re.match(r"\s+Codecs\s+:\s+\(([\w\|]*?)\)", codec_line).group(1).split('|')
    return codec in codec_list


@step(u'Then the codec "([^"]*)" appears after typing \'sip show peer\' in asterisk')
def then_the_codec_appears_after_typing_sip_show_peer_in_asterisk(step, codec):
    assert check_codec_for_sip_line(world.id, codec) is True


@step(u'Then the codec "([^"]*)" does not appear after typing \'sip show peer\' in asterisk')
def then_the_codec_does_not_appear_after_typing_sip_show_peer_in_asterisk(step, codec):
    assert check_codec_for_sip_line(world.id, codec) is False


@step(u'Then the line with number "([^"]*)" has the codec "([^"]*)"')
def then_the_line_with_number_group1_has_the_codec_group2(step, linenumber, codec):
    line = line_helper.find_with_exten_context(linenumber, 'default')
    sip_peer = line.name
    assert check_codec_for_sip_line(sip_peer, codec)


@step(u'Then this line is displayed in the list')
def then_this_line_is_displayed_in_the_list(step):
    common.open_url('line', 'search', {'search': world.id})
    assert common.find_line(world.id) is not None
    common.open_url('line', 'search', {'search': ''})


@step(u'Then this line is not displayed in the list')
def then_this_line_is_not_displayed_in_the_list(step):
    common.open_url('line', 'search', {'search': world.id})
    assert common.find_line(world.id) is None
    common.open_url('line', 'search', {'search': ''})


@step(u'Then the line "([^"]*)" has the following line options:')
def then_the_line_1_has_the_following_line_options(step, line_number):
    line_id = line_helper.find_line_id_with_exten_context(line_number, 'default')
    common.open_url('line', 'edit', {'id': line_id})
    for line_data in step.hashes:
        for key, value in line_data.iteritems():
            if key == 'Call limit':
                common.go_to_tab('IPBX Infos')
                assert line_action_webi.get_value_from_ipbx_infos_tab('call_limit') == value
            elif key == 'NAT':
                common.go_to_tab('General')
                nat_select = world.browser.find_element_by_label('NAT')
                nat_value = Select(nat_select).first_selected_option.text
                assert nat_value == value
            elif key == 'IP addressing type':
                common.go_to_tab('Advanced')
                ip_addressing_type_select = world.browser.find_element_by_label('IP Addressing type')
                ip_addressing_type_value = Select(ip_addressing_type_select).first_selected_option.text
                assert ip_addressing_type_value == value
            elif key == 'IP address':
                common.go_to_tab('Advanced')
                ip_address_input = world.browser.find_element_by_label('IP address')
                ip_address_value = ip_address_input.get_attribute('value')
                assert ip_address_value == value
            elif key == 'Caller ID':
                common.go_to_tab('IPBX Infos')
                assert line_action_webi.get_value_from_ipbx_infos_tab('callerid') == value
            else:
                raise Exception('%s is not a valid key' % key)


@step(u'Then I see the line "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    common.open_url('line', 'search', {'search': name})
    line = common.find_line(name)
    common.open_url('line', 'search', {'search': ''})
    assert line is not None, 'Line: %s does not exist' % name


@step(u'Then I see the line "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    common.open_url('line', 'search', {'search': name})
    line = common.find_line(name)
    common.open_url('line', 'search', {'search': ''})
    assert line is None, 'Line: %s exist' % name


def _add_codec_to_line(codec, exten):
    _add_codec_list_to_line([codec], exten)


def _add_codec_list_to_line(codecs, exten):
    line_id = line_helper.find_line_id_with_exten_context(exten, 'default')
    common.open_url('line', 'edit', {'id': line_id})
    for codec in codecs:
        _add_custom_codec(codec)
    form.submit.submit_form()


def _open_codec_page():
    try:
        common.go_to_tab('Signalling')
    except NoSuchElementException:
        # SCCP line has no Signalling tab
        return


@step(u'Then the line "([^"]*)" no longer exists')
def then_the_line__no_longer_exists(step, line_id):
    response = line_action_restapi.get(line_id)
    assert_that(response.status, equal_to(404))


@step(u'Then the line sip "([^"]*)" no longer exists')
def then_the_line_sip_no_longer_exists(step, line_id):
    response = line_sip_action_restapi.get(line_id)
    assert_that(response.status, equal_to(404))


@step(u'Then I get a list containing the following lines:')
def then_i_get_a_list_containing_the_following_lines(step):
    line_response = world.response.data
    expected_lines = step.hashes

    assert_that(line_response, has_key('items'))
    lines = line_response['items']

    for expected_line in expected_lines:
        expected_line = _convert_line_parameters(expected_line)
        assert_that(lines, has_item(has_entries(expected_line)))


def _convert_line_parameters(line):

    if 'id' in line:
        line['id'] = int(line['id'])

    if 'device_slot' in line:
        line['device_slot'] = int(line['device_slot'])

    return line


@step(u'Then I get a line with the following parameters:')
def then_i_get_a_line_with_the_following_parameters(step):
    expected_line = _convert_line_parameters(step.hashes[0])
    line_response = world.response.data

    assert_that(line_response, has_entries(expected_line))


@step(u'Then I have a line_sip with the following parameters:')
def then_i_have_an_line_sip_with_the_following_parameters(step):
    parameters = _extract_line_parameters(step)
    line = world.response.data

    assert_that(line, has_entries(parameters))


def _extract_line_parameters(step):
    parameters = step.hashes[0]

    if 'id' in parameters:
        parameters['id'] = int(parameters['id'])

    return parameters


@step(u'Then I have a line_sip with the following attributes:')
def then_i_have_an_line_sip_with_the_following_attributes(step):
    line = world.response.data

    for line_attribute in step.hashes:
        assert_that(line.keys(), has_item(line_attribute['attribute']))
