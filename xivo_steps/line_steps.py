# -*- coding: utf-8 -*-

from lettuce import step, world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from xivo_lettuce import common
from xivo_lettuce.common import find_line, open_url, remove_all_elements, \
    remove_line, edit_line
from xivo_lettuce.manager_ws import line_manager_ws
from xivo_lettuce.manager import line_manager
from xivo_lettuce import form
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.form.list_pane import ListPane


@step(u'Given there is no custom lines')
def given_there_is_no_custom_lines(step):
    remove_all_elements('line', 'Customized')


@step(u'Given I set the following options in line "([^"]*)":')
def given_i_set_the_following_options_in_line_1(step, line_number):
    line_id = line_manager_ws.find_line_id_with_number(line_number, 'default')
    open_url('line', 'edit', {'id': line_id})

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


@step(u'When I add a "([^"]*)" line')
def when_i_add_a_line(step, protocol):
    open_url('line', 'add', {'proto': protocol.lower()})
    if protocol.lower() == 'sip':
        world.id = world.browser.find_element_by_id('it-protocol-name').get_attribute('value')


@step(u'When I set the context to "([^"]*)"')
def when_i_set_the_context(step, context):
    select_context = world.browser.find_element_by_xpath(
        '//select[@id="it-protocol-context"]//option[@value="%s"]' % context)
    select_context.click()


@step(u'When I set the interface to "([^"]*)"')
def when_i_set_the_interface(step, interface):
    input_interface = world.browser.find_element_by_id('it-protocol-interface')
    input_interface.send_keys(interface)


@step(u'When I remove this line')
def when_i_remove_this_line(step):
    open_url('line', 'search', {'search': world.id})
    remove_line(world.id)
    open_url('line', 'search', {'search': ''})


@step(u'When I search for this line')
def when_i_search_for_this_line(step):
    line_manager.search_line_number(world.id)


@step(u'When I edit this line')
def when_i_edit_this_line(step):
    edit_line(world.id)


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    line_id = line_manager_ws.find_line_id_with_number(linenumber, 'default')
    open_url('line', 'edit', {'id': line_id})


@step(u'When I activate custom codecs')
def when_i_activate_custom_codecs(step):
    Checkbox.from_label("Customize codecs:").check()


@step(u'When I deactivate custom codecs')
def when_i_deactivate_custom_codecs(step):
    Checkbox.from_label("Customize codecs:").uncheck()


@step(u'When I add the codec "([^"]*)"')
def when_i_add_the_codec(step, codec):
    list_pane = ListPane.from_id('codeclist')
    list_pane.add(codec)


def check_codec_for_sip_line(peer, codec):
    command = ['asterisk', '-rx', '"sip show peer %s"' % peer]
    output = world.ssh_client_xivo.out_call(command)
    codec_line = [x for x in output.split("\n") if 'Codecs' in x][0]
    return ('(%s)' % codec) in codec_line


@step(u'Then the codec "([^"]*)" appears after typing \'sip show peer\' in asterisk')
def then_the_codec_appears_after_typing_sip_show_peer_in_asterisk(step, codec):
    assert check_codec_for_sip_line(world.id, codec) is True


@step(u'Then the codec "([^"]*)" does not appear after typing \'sip show peer\' in asterisk')
def then_the_codec_does_not_appear_after_typing_sip_show_peer_in_asterisk(step, codec):
    assert check_codec_for_sip_line(world.id, codec) is False


@step(u'Then this line is displayed in the list')
def then_this_line_is_displayed_in_the_list(step):
    open_url('line', 'search', {'search': world.id})
    assert find_line(world.id) is not None
    open_url('line', 'search', {'search': ''})


@step(u'Then this line is not displayed in the list')
def then_this_line_is_not_displayed_in_the_list(step):
    open_url('line', 'search', {'search': world.id})
    try:
        find_line(world.id)
    except NoSuchElementException:
        pass
    else:
        assert False
    open_url('line', 'search', {'search': ''})


@step(u'^Then I see in IPBX Infos tab value "([^"]*)" has set to (.*)$')
def then_i_see_the_value_has_set_to(step, var_name, var_val):
    expected_var_val = line_manager.get_value_from_ipbx_infos_tab(var_name)
    assert expected_var_val == var_val


@step(u'Then the line "([^"]*)" has the following line options:')
def then_the_line_1_has_the_following_line_options(step, line_number):
    line_id = line_manager_ws.find_line_id_with_number(line_number, 'default')
    open_url('line', 'edit', {'id': line_id})
    for line_data in step.hashes:
        for key, value in line_data.iteritems():
            if key == 'Call limit':
                common.go_to_tab('IPBX Infos')
                assert line_manager.get_value_from_ipbx_infos_tab('call_limit') == value
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
            else:
                raise Exception('%s is not a valid key' % key)