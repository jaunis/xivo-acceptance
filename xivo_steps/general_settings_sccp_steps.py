# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce import form
from xivo_lettuce.form import submit
from xivo_lettuce.form.checkbox import Checkbox
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import asterisk_manager
from xivo_lettuce.manager_ws import general_settings_sccp_manager_ws as sccp_manager_ws
from selenium.webdriver.support.select import Select


@step(u'Given the SCCP directmedia is disabled')
def given_the_sccp_directmedia_is_disabled(step):
    sccp_manager_ws.disable_directmedia()


@step(u'Given the SCCP directmedia is enabled')
def given_the_sccp_directmedia_is_enabled(step):
    sccp_manager_ws.enable_directmedia()


@step(u'Given the SCCP dial timeout is at "(\d+)" seconds')
def given_the_sccp_dial_timeout_is_at_1_seconds(step, timeout):
    sccp_manager_ws.set_dialtimeout(timeout)


@step(u'Given the SCCP language is "([^"]*)"')
def given_the_sccp_language_is_1(step, language):
    sccp_manager_ws.set_language(language)


@step(u'When I enable the SCCP directmedia')
def when_i_enable_the_sccp_directmedia(step):
    open_url('sccpgeneralsettings')
    directmedia_checkbox = Checkbox.from_id("it-sccpgeneralsettings-directmedia")
    directmedia_checkbox.check()
    form.submit.submit_form()


@step(u'When I disable the SCCP directmedia')
def when_i_disable_the_sccp_directmedia(step):
    open_url('sccpgeneralsettings')
    directmedia_checkbox = Checkbox.from_id("it-sccpgeneralsettings-directmedia")
    directmedia_checkbox.uncheck()
    submit.submit_form()


@step(u'When I change the SCCP dial timeout to "([^"]*)" seconds')
def when_i_change_the_sccp_dial_timeout_to_1_seconds(step, timeout):
    open_url('sccpgeneralsettings')
    form.input.set_text_field_with_id('it-sccpgeneralsettings-dialtimeout', timeout)
    form.submit.submit_form()


@step(u'When I select the SCCP language "([^"]*)"')
def when_i_select_the_sccp_language_group1(step, language):
    open_url('sccpgeneralsettings')
    form.select.set_select_field_with_id('it-sccpgeneralsettings-language', language)
    form.submit.submit_form()


@step('Then the option "([^"]*)" is at "([^"]*)" in sccp.conf')
def then_the_option_is_at_x_in_sccp_conf(step, option, expected_value):
    value = asterisk_manager.get_asterisk_conf("sccp.conf", option)
    assert(value == expected_value)
