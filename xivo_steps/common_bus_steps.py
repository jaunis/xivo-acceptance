# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import json
import pika

from lettuce import step
from lettuce.registry import world


@step(u'Given I listen on the bus for messages:')
def given_i_listen_on_the_bus_for_messages(step):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=world.config.xivo_host))
    channel = connection.channel()

    for entry in step.hashes:
        try:
            exchange = entry['exchange'].encode('ascii')
            routing_key = entry['routing_key'].encode('ascii')
            queue_name = 'test_%s' % routing_key
            result = channel.queue_declare(queue=queue_name)
            queue_name = result.method.queue

            channel.queue_bind(exchange=exchange,
                               queue=queue_name,
                               routing_key=routing_key)
        finally:
            connection.close()


@step(u'Then I see a message on bus with the following variables:')
def then_i_see_a_message_on_bus_with_the_following_variables(step):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=world.config.xivo_host))
    channel = connection.channel()
    queue_name = 'test_call_form_result'

    def callback(ch, method, props, body):
        unmarshaled_body = json.loads(body)
        data = unmarshaled_body['data']['variables']

        for expected_widget in step.hashes:
            widget_name = expected_widget['widget_name']
            widget_value = expected_widget['value']
            assert(unicode(data[widget_name]) == widget_value)

    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    connection.process_data_events()
    connection.close()
