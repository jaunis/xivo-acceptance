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

from lettuce import step
from hamcrest import *

from xivo_acceptance.helpers import cti_helper


@step(u'Then the agent list xlet shows agent "([^"]*)" as in use')
def then_the_agent_list_xlet_shows_agent_as_in_use(step, agent_number):
    agent = _get_agent_infos(agent_number)

    assert_that(agent['availability'], starts_with('In use'), 'agent %s not "In use"' % agent_number)


@step(u'Then the agent list xlet shows agent "([^"]*)" as on incoming non-ACD call')
def then_the_agent_list_xlet_shows_agent_as_on_non_acd_call(step, agent_number):
    agent = _get_agent_infos(agent_number)

    assert_that(agent['availability'], starts_with('Ext. Incoming'), 'agent %s not "OOQ In"' % agent_number)


@step(u'Then the agent list xlet shows agent "([^"]*)" as not in use')
def then_the_agent_list_xlet_shows_agent_as_not_in_use(step, agent_number):
    agent = _get_agent_infos(agent_number)

    assert_that(agent['availability'], starts_with('Not in use'), 'agent %s not "Not in use"' % agent_number)


@step(u'Then the agent list xlet shows agent "([^"]*)" as unlogged')
def then_the_agent_list_xlet_shows_agent_as_unlogged(step, agent_number):
    agent = _get_agent_infos(agent_number)

    assert_that(agent['availability'], starts_with('-'), 'agent %s not "Unlogged"' % agent_number)


def _get_agent_infos(agent_number):
    agent_list_infos = cti_helper.get_agent_list_infos()
    agent_list = agent_list_infos['content']
    agent_list = [agent for agent in agent_list if agent['number'] == agent_number]

    assert_that(len(agent_list), greater_than(0), 'agent %s not found in xlet agent list' % agent_number)
    assert_that(len(agent_list), less_than(2), 'more than one agent %s found in xlet agent list' % agent_number)

    return agent_list[0]
