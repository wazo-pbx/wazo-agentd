# Copyright (C) 2013-2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

import logging

from xivo import debug
from xivo_dao.helpers import db_utils

logger = logging.getLogger(__name__)


class LogoffHandler(object):

    def __init__(self, logoff_manager, agent_status_dao):
        self._logoff_manager = logoff_manager
        self._agent_status_dao = agent_status_dao

    @debug.trace_duration
    def handle_logoff_by_id(self, agent_id):
        logger.info('Executing logoff command (ID %s)', agent_id)
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status(agent_id)
        self._handle_logoff(agent_status)

    @debug.trace_duration
    def handle_logoff_by_number(self, agent_number):
        logger.info('Executing logoff command (number %s)', agent_number)
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status_by_number(agent_number)
        self._handle_logoff(agent_status)

    @debug.trace_duration
    def handle_logoff_all(self):
        logger.info('Executing logoff all command')
        self._logoff_manager.logoff_all_agents()

    def _handle_logoff(self, agent_status):
        self._logoff_manager.logoff_agent(agent_status)
