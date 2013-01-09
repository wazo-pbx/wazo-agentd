# -*- coding: UTF-8 -*-

# Copyright (C) 2012-2013  Avencall
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

import unittest
from mock import Mock, patch
from xivo_agent.ctl.client import AgentClient, _AgentStatus


class TestAgentClient(unittest.TestCase):

    def setUp(self):
        self.agent_client = AgentClient()

    @patch('xivo_agent.ctl.commands.AddToQueueCommand')
    def test_add_agent_to_queue(self, AddToQueueCommand):
        agent_id = 42
        queue_id = 1
        command = Mock()
        AddToQueueCommand.return_value = command
        self.agent_client._execute_command = Mock()

        self.agent_client.add_agent_to_queue(agent_id, queue_id)

        AddToQueueCommand.assert_called_once_with(agent_id, queue_id)
        self.agent_client._execute_command.assert_called_once_with(command)

    @patch('xivo_agent.ctl.commands.RemoveFromQueueCommand')
    def test_remove_agent_from_queue(self, RemoveFromQueueCommand):
        agent_id = 42
        queue_id = 1
        command = Mock()
        RemoveFromQueueCommand.return_value = command
        self.agent_client._execute_command = Mock()

        self.agent_client.remove_agent_from_queue(agent_id, queue_id)

        RemoveFromQueueCommand.assert_called_once_with(agent_id, queue_id)
        self.agent_client._execute_command.assert_called_once_with(command)

    @patch('xivo_agent.ctl.client.AMQPTransportClient')
    def test_connect_no_transport(self, amqp_client_constructor):
        hostname = 'localhost'
        port = 5672

        client = AgentClient()
        client.connect(hostname, port)
        amqp_client_constructor.create_and_connect.assert_called_once_with(hostname, port)

    @patch('xivo_agent.ctl.client.AMQPTransportClient')
    def test_connect_already_connected(self, amqp_client_constructor):
        hostname = 'localhost'
        port = 5672

        client = AgentClient()
        client.connect(hostname, port)
        self.assertRaises(Exception, client.connect, hostname, port)

    @patch('xivo_agent.ctl.commands.StatusesCommand')
    def test_get_agent_statuses(self, StatusesCommand):
        agent1 = {
            'id': 1,
            'number': '1001',
            'extension': '9001',
            'context': 'default',
            'logged': True,
        }

        agent2 = {
            'id': 2,
            'number': '1002',
            'extension': None,
            'context': None,
            'logged': False,
        }

        command = Mock()
        StatusesCommand.return_value = command

        execute_command = Mock()
        execute_command.return_value = [agent1, agent2]
        self.agent_client._execute_command = execute_command

        statuses = self.agent_client.get_agent_statuses()

        self.assertTrue(isinstance(statuses[0], _AgentStatus))
        self.assertEquals(statuses[0].id, agent1['id'])
        self.assertEquals(statuses[0].number, agent1['number'])
        self.assertEquals(statuses[0].extension, agent1['extension'])
        self.assertEquals(statuses[0].context, agent1['context'])
        self.assertEquals(statuses[0].logged, agent1['logged'])

        self.assertTrue(isinstance(statuses[1], _AgentStatus))
        self.assertEquals(statuses[1].id, agent2['id'])
        self.assertEquals(statuses[1].number, agent2['number'])
        self.assertEquals(statuses[1].extension, agent2['extension'])
        self.assertEquals(statuses[1].context, agent2['context'])
        self.assertEquals(statuses[1].logged, agent2['logged'])

        StatusesCommand.assert_called_once_with()
        self.agent_client._execute_command.assert_called_once_with(command)

    @patch('xivo_agent.ctl.commands.StatusCommand')
    def test_get_agent_status_by_number(self, StatusCommand):
        agent = {
            'id': 1,
            'number': '1001',
            'extension': '9001',
            'context': 'default',
            'logged': True,
        }

        agent_number = '1001'

        command = Mock()
        StatusCommand.return_value.by_number.return_value = command

        execute_command = Mock()
        execute_command.return_value = agent
        self.agent_client._execute_command = execute_command

        status = self.agent_client.get_agent_status_by_number(agent_number)

        self.assertTrue(isinstance(status, _AgentStatus))
        self.assertEquals(status.id, agent['id'])
        self.assertEquals(status.number, agent['number'])
        self.assertEquals(status.extension, agent['extension'])
        self.assertEquals(status.context, agent['context'])
        self.assertEquals(status.logged, agent['logged'])

        StatusCommand.assert_called_once_with()
        self.agent_client._execute_command.assert_called_once_with(command)