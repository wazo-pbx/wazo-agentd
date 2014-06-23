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

from xivo_agent.exception import AgentAlreadyInQueueError


class AddMemberManager(object):

    def __init__(self, add_to_queue_action, ami_client, agent_status_dao, queue_member_dao):
        self._add_to_queue_action = add_to_queue_action
        self._ami_client = ami_client
        self._agent_status_dao = agent_status_dao
        self._queue_member_dao = queue_member_dao

    def add_agent_to_queue(self, agent, queue):
        self._check_agent_is_not_member_of_queue(agent, queue)
        self._add_queue_member(agent, queue)
        self._send_agent_added_event(agent, queue)
        self._add_to_queue_if_logged(agent, queue)

    def _check_agent_is_not_member_of_queue(self, agent, queue):
        for agent_queue in agent.queues:
            if agent_queue.name == queue.name:
                raise AgentAlreadyInQueueError()

    def _add_queue_member(self, agent, queue):
        self._queue_member_dao.add_agent_to_queue(agent.id, agent.number, queue.name)

    def _send_agent_added_event(self, agent, queue):
        self._ami_client.agent_added_to_queue(agent.id, agent.number, queue.name)

    def _add_to_queue_if_logged(self, agent, queue):
        agent_status = self._agent_status_dao.get_status(agent.id)
        if agent_status is not None:
            self._add_to_queue_action.add_agent_to_queue(agent_status, queue)