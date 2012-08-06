# -*- coding: UTF-8 -*-

import time
from lettuce.decorators import step
from xivo_lettuce.manager import queuelog_manager, queue_manager, agent_manager
from xivo_lettuce.manager.context_manager import add_contextnumbers_queue


@step(u'Given there is a queue "([^"]*)" in context "([^"]*)" with number "([^"]*)"$')
def given_there_is_a_queue_in_context_with_number(step, name, context, number):
    add_contextnumbers_queue(context, number, number)
    agent_manager.insert_agent('test', 'test', '7878', '')
    agent_id = agent_manager.find_agent_id_from_number('7878')
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 0,
            'agents': agent_id}
    queue_manager.insert_queue(data)


@step(u'Given there is no queue with name "([^"]+)"')
def given_there_is_no_queue_with_name(step, queue_name):
    queue_manager.delete_queue_from_displayname(queue_name)


@step(u'Given there is no queue with number "([^"]*)"')
def given_there_is_no_queue_with_number(step, queue_number):
    queue_manager.delete_queue_from_number(queue_number)


@step(u'Given there is no "([^"]*)" entry in queue "([^"]*)')
def given_there_is_no_event_entry_in_queue_log_table_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'Then i should see ([0-9]+) "([^"]*)" calls in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_group1_calls_in_queue_group2_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert(count == int(expected_count))


@step(u'Given I wait ([0-9]+) seconds for the dialplan to be reloaded')
def given_i_wait_n_seconds_for_the_dialplan_to_be_reloaded(step, count):
    time.sleep(int(count))