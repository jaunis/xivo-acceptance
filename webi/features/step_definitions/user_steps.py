# -*- coding: utf-8 -*-

import xivo_ws
import time

from lettuce import step
from lettuce.registry import world
from selenium.webdriver.support.select import Select
from xivo_lettuce.manager import user_manager as user_man
from xivo_lettuce.manager import line_manager as line_man
from xivo_lettuce.common import open_url, submit_form, element_is_in_list, \
    remove_line, edit_line, go_to_tab, find_line


@step(u'Given there is a user "([^"]*)" "([^"]*)"$')
def given_there_is_a_user_1_2(step, firstname, lastname):
    user_man.delete_user(firstname, lastname)
    user_man.insert_user(firstname, lastname)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with no line$')
def given_there_is_a_user_1_2_with_no_line(step, firstname, lastname):
    user_man.delete_user(firstname, lastname)
    user_man.insert_user_with_no_line(firstname, lastname)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    user_man.delete_user(firstname, lastname)


@step(u'I add a user$')
def i_add_a_user(step):
    open_url('user', 'add')


@step(u'When I create a user "([^"]*)" "([^"]*)"$')
def when_i_create_a_user(step, firstname, lastname):
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    submit_form()


@step(u'When I add user "([^"]*)" "([^"]*)" in group "([^"]*)"')
def when_i_create_a_user_in_group(step, firstname, lastname, group):
    import group_steps as grp
    grp.when_i_create_group(step, group)
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    user_man.type_user_in_group(group)
    submit_form()
    element_is_in_list('user', '%s %s' % (firstname, lastname))


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    id = user_man.find_user_id(orig_firstname, orig_lastname)
    user_man.delete_user(dest_firstname, dest_lastname)
    if len(id) > 0:
        open_url('user', 'edit', {'id': id[0]})
        user_man.type_user_names(dest_firstname, dest_lastname)
        submit_form()


@step(u'When I remove user "([^"]*)" "([^"]*)"')
def remove_user(step, firstname, lastname):
    remove_line('%s %s' % (firstname, lastname))


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id_list = user_man.find_user_id(firstname, lastname)
    time.sleep(3)
    if len(user_id_list) > 0:
        assert user_man.is_in_group(group_name, user_id_list[0])


@step(u'Given a user "([^"]*)" "([^"]*)" in group "([^"]*)"')
def given_a_user_in_group(step, firstname, lastname, group):
    user_man.delete_user(firstname, lastname)
    user_man.insert_user(firstname, lastname)
    user_man.insert_group_with_user(group, user_man.find_user_id(firstname, lastname))


@step(u'Then I should be at the user list page')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)"$')
def given_there_is_a_user_1_2_with_a_sip_line_3(step, firstname, lastname, linenumber):
    user_man.delete_user(firstname, lastname)
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    user_man.user_form_add_line(linenumber)
    submit_form()


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)" in group "([^"]*)"')
def given_there_is_a_user_1_2_with_a_sip_line_3_in_group_4(step, firstname, lastname, linenumber, group_name):
    user_man.delete_user(firstname, lastname)
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    user_man.type_user_in_group(group_name)
    user_man.user_form_add_line(linenumber)
    submit_form()


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    line_ids = line_man.find_line_id_from_number(linenumber, 'default')
    if len(line_ids) > 0:
        open_url('line', 'edit', {'id': line_ids[0]})


@step(u'I edit the user "([^"]*)" "([^"]*)"')
def when_i_edit_the_user_1_2(step, firstname, lastname):
    open_url('user', 'list')
    edit_line('%s %s' % (firstname, lastname))


@step(u'Then I see the line "([^"]*)" has its call limit to "([^"]*)"')
def then_i_see_the_line_1_has_its_call_limit_to_2(step, line_number, call_limit):
    line_id = line_man.find_line_id_from_number(line_number, 'default')[0]
    open_url('line', 'edit', {'id': line_id})

    go_to_tab('IPBX Infos')

    key = 'call_limit'
    value_cell = world.browser.find_element_by_xpath(
        "//table"
        "//tr[td[@class = 'td-left' and text() = '%s']]"
        "//td[@class = 'td-right']"
        % key)
    assert value_cell.text == call_limit


@step(u'I enable the XiVO Client as "([^"]*)" pass "([^"]*)" profile "([^"]*)"')
def i_enable_the_xivo_client_as_1_pass_2_profile_3(step, login, password, profile):
    step.given('Given the option "Enable XiVO Client" is checked')
    step.given('I set the text field "Login" to "%s"' % login)
    step.given('I set the text field "Password" to "%s"' % password)
    step.given('I set the select field "Profile" to "%s"' % profile)


@step(u'I add a SIP line "([^"]*)" to the user')
def given_i_add_a_sip_line_1(step, linenumber):
    user_man.user_form_add_line(linenumber)


@step(u'I add a voicemail "([^"]*)"')
def i_add_a_voicemail_1_on_2(step, vm_num):
    go_to_tab('Voicemail')
    step.given('I set the select field "Voice Mail" to "Asterisk"')
    step.given('Given the option "Enable voicemail" is checked')
    step.given('I set the text field "Voicemail" to "%s"' % vm_num)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)", voicemail and CTI profile "([^"]*)"')
def given_i_there_is_a_user_1_2_with_a_sip_line_3_voicemail_and_cti_4_profile(step, first_name, last_name, line_number, cti_profile):
    user = xivo_ws.User()
    user.firstname = first_name
    user.lastname = last_name
    user.language = 'en_US'
    user.line = xivo_ws.UserLine(number=int(line_number),
                                 context='default')
    user.voicemail = xivo_ws.UserVoicemail(number=int(line_number),
                                           name=line_number)
    user.enable_client = True
    user.client_username = first_name.lower()
    user.client_password = last_name.lower()
    user.client_profile = cti_profile

    world.ws.users.add(user)

    time.sleep(world.timeout)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)" and CTI profile "([^"]*)"')
def given_there_is_a_user_1_2_with_a_sip_line_3_and_cti_profile_4(step, first_name, last_name, line_number, cti_profile):
    user = xivo_ws.User()
    user.firstname = first_name
    user.lastname = last_name
    user.line = xivo_ws.UserLine(number=int(line_number),
                                 context='default')
    user.enable_client = True
    user.client_username = first_name.lower()
    user.client_password = last_name.lower()
    user.client_profile = cti_profile

    world.ws.users.add(user)

    time.sleep(world.timeout)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with an agent "([^"]*)" and CTI profile "([^"]*)"')
def given_there_is_a_user_1_2_with_an_agent_3_and_cti_profile_4(step, first_name, last_name, agent_number, cti_profile):
    user = xivo_ws.User()
    user.firstname = first_name
    user.lastname = last_name
    user.enable_client = True
    user.client_username = first_name.lower()
    user.client_password = last_name.lower()
    user.client_profile = cti_profile
    user_id = world.ws.users.add(user)

    agent = xivo_ws.Agent()
    agent.firstname = first_name
    agent.lastname = last_name
    agent.number = int(agent_number)
    agent.context = 'default'
    agent.users = [int(user_id)]

    world.ws.agents.add(agent)

    time.sleep(world.timeout)


@step(u'When I delete agent number "([^"]*)"')
def when_i_delete_agent_number_1(step, agent_number):
    agent = world.ws.agents.search(agent_number)[0]
    world.ws.agents.delete(agent.id)

    time.sleep(world.timeout)


@step(u'When I add a user "([^"]*)" "([^"]*)" with a function key with type Customized and extension "([^"]*)"')
def when_i_add_a_user_group1_group2_with_a_function_key(step, firstname, lastname, extension):
    user_man.delete_user(firstname, lastname)
    open_url('user', 'add')

    user_man.type_user_names(firstname, lastname)
    user_man.type_func_key('Customized', extension)

    submit_form()


@step(u'Then I see the user "([^"]*)" "([^"]*)" exists')
def then_i_see_the_user_group1_group2_exists(step, firstname, lastname):
    open_url('user', 'list')
    user_line = find_line("%s %s" % (firstname, lastname))
    assert user_line is not None


@step(u'Then i see user with username "([^"]*)" "([^"]*)" has a function key with type Customized and extension "([^"]*)"')
def then_i_see_user_with_username_group1_group2_has_a_function_key(step, firstname, lastname, extension):
    edit_line("%s %s" % (firstname, lastname))
    go_to_tab('Func Keys')
    destination_field = world.browser.find_element_by_id('it-phonefunckey-custom-typeval-0')
    assert destination_field.get_attribute('value') == extension
    type_field = Select(world.browser.find_element_by_id('it-phonefunckey-type-0'))
    assert type_field.first_selected_option.text == "Customized"


@step(u'When I remove line "([^"]*)" from user')
def when_i_remove_line_from_user(step, lineNumber):
    go_to_tab('Lines')
    select_line = world.browser.find_element_by_xpath("//table[@id='list_linefeatures']/tbody/tr//input[@id='linefeatures-number' and @value='%s']" % lineNumber)
    delete_button = select_line.find_element_by_xpath("//a[@title='Delete this line']")
    delete_button.click()
    time.sleep(world.timeout)


@step(u'When I remove line "([^"]*)" from lines')
def when_i_remove_line_from_lines(step, line_number):
    open_url('line')
    line_man.search_line_number(line_number)
    remove_line(line_number)
    time.sleep(world.timeout)
    line_man.unsearch_line()
